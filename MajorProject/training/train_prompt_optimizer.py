#!/usr/bin/env python3
"""Fine-tune FLAN-T5 for prompt optimization."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
    set_seed,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training.config import (  # noqa: E402
    BATCH_SIZE,
    DATASET_PATH,
    EVAL_BATCH_SIZE,
    EVAL_STRATEGY,
    FP16,
    GRADIENT_ACCUMULATION_STEPS,
    GREATER_IS_BETTER,
    LEARNING_RATE,
    LOAD_BEST_MODEL_AT_END,
    LOGGING_STEPS,
    LOGS_DIR,
    MAX_INPUT_LENGTH,
    MAX_TARGET_LENGTH,
    METRIC_FOR_BEST_MODEL,
    MODEL_NAME,
    NUM_EPOCHS,
    OUTPUT_DIR,
    RANDOM_SEED,
    SAVE_STRATEGY,
    SAVE_TOTAL_LIMIT,
    TASK_PREFIX,
    TEST_RATIO,
    TRAIN_RATIO,
    VAL_RATIO,
    WARMUP_RATIO,
    WEIGHT_DECAY,
)
from training.evaluate_model import compute_metrics, save_metrics  # noqa: E402
from training.progress import PhaseProgress, TrainingProgressCallback  # noqa: E402

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOGS_DIR / "training.log"),
        ],
    )


def load_and_split_dataset() -> tuple[Dataset, Dataset, Dataset]:
    frame = pd.read_csv(DATASET_PATH)
    frame = frame.dropna(subset=["original_prompt", "optimized_prompt"])
    frame["original_prompt"] = frame["original_prompt"].astype(str).str.strip()
    frame["optimized_prompt"] = frame["optimized_prompt"].astype(str).str.strip()
    frame = frame[frame["original_prompt"].str.len() > 0]
    frame = frame[frame["optimized_prompt"].str.len() > 0]

    train_df, temp_df = train_test_split(
        frame,
        test_size=(1 - TRAIN_RATIO),
        random_state=RANDOM_SEED,
        shuffle=True,
    )
    relative_test = TEST_RATIO / (VAL_RATIO + TEST_RATIO)
    val_df, test_df = train_test_split(
        temp_df,
        test_size=relative_test,
        random_state=RANDOM_SEED,
        shuffle=True,
    )

    logger.info(
        "Dataset split: train=%d val=%d test=%d",
        len(train_df),
        len(val_df),
        len(test_df),
    )

    return (
        Dataset.from_pandas(train_df.reset_index(drop=True)),
        Dataset.from_pandas(val_df.reset_index(drop=True)),
        Dataset.from_pandas(test_df.reset_index(drop=True)),
    )


def preprocess_function(examples, tokenizer, prefix: str):
    inputs = [prefix + text for text in examples["original_prompt"]]
    model_inputs = tokenizer(
        inputs,
        max_length=MAX_INPUT_LENGTH,
        truncation=True,
    )
    labels = tokenizer(
        text_target=examples["optimized_prompt"],
        max_length=MAX_TARGET_LENGTH,
        truncation=True,
    )
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


def export_to_onnx(model, tokenizer, export_dir: Path) -> bool:
    export_dir.mkdir(parents=True, exist_ok=True)
    try:
        from optimum.onnxruntime import ORTModelForSeq2SeqLM

        onnx_model = ORTModelForSeq2SeqLM.from_pretrained(
            str(OUTPUT_DIR),
            export=True,
        )
        onnx_model.save_pretrained(export_dir)
        tokenizer.save_pretrained(export_dir)
        logger.info("ONNX export saved to %s", export_dir)
        return True
    except Exception as exc:
        logger.warning("ONNX export failed: %s", exc)
        try:
            import torch.onnx

            dummy_input = tokenizer(
                TASK_PREFIX + "Can you please explain AI in detail?",
                return_tensors="pt",
                max_length=MAX_INPUT_LENGTH,
                truncation=True,
            )
            onnx_path = export_dir / "model.onnx"
            torch.onnx.export(
                model,
                tuple(dummy_input.values()),
                onnx_path,
                input_names=list(dummy_input.keys()),
                output_names=["logits"],
                dynamic_axes={name: {0: "batch", 1: "sequence"} for name in dummy_input},
                opset_version=14,
            )
            tokenizer.save_pretrained(export_dir)
            logger.info("Fallback ONNX export saved to %s", onnx_path)
            return True
        except Exception as fallback_exc:
            logger.warning("Fallback ONNX export failed: %s", fallback_exc)
            return False


def safe_batch_decode(tokenizer, token_ids) -> list[str]:
    """Decode generated IDs safely for evaluation.

    With predict_with_generate=True this is usually already token IDs, but some
    Transformers versions return a tuple, logits, or include -100 / OOV values
    that crash tokenizer.batch_decode with OverflowError.
    """
    preds = token_ids
    if isinstance(preds, tuple):
        preds = preds[0]
    preds = np.asarray(preds)
    if preds.ndim == 3:
        preds = np.argmax(preds, axis=-1)

    preds = preds.astype(np.int64, copy=False)
    pad_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else 0
    vocab_size = len(tokenizer)

    # -100 is the HF ignore index; negative / OOV IDs also cause OverflowError.
    preds = np.where(preds < 0, pad_id, preds)
    preds = np.where(preds >= vocab_size, pad_id, preds)

    return tokenizer.batch_decode(preds, skip_special_tokens=True)


def run_test_evaluation(trainer, tokenized_test, raw_test_dataset, tokenizer) -> dict:
    predictions = trainer.predict(tokenized_test)
    decoded_preds = safe_batch_decode(tokenizer, predictions.predictions)
    sources = raw_test_dataset["original_prompt"]
    references = raw_test_dataset["optimized_prompt"]
    return compute_metrics(decoded_preds, references, sources, tokenizer)


def main() -> None:
    setup_logging()
    set_seed(RANDOM_SEED)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and torch.backends.mps.is_available():
        device = "mps"
    logger.info("Using device: %s", device)

    train_dataset, val_dataset, test_dataset = load_and_split_dataset()

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

    print("\n[1/4] Tokenizing datasets...")
    tokenized_train = train_dataset.map(
        lambda batch: preprocess_function(batch, tokenizer, TASK_PREFIX),
        batched=True,
        remove_columns=train_dataset.column_names,
        desc="Tokenize train",
    )
    tokenized_val = val_dataset.map(
        lambda batch: preprocess_function(batch, tokenizer, TASK_PREFIX),
        batched=True,
        remove_columns=val_dataset.column_names,
        desc="Tokenize validation",
    )
    tokenized_test = test_dataset.map(
        lambda batch: preprocess_function(batch, tokenizer, TASK_PREFIX),
        batched=True,
        remove_columns=test_dataset.column_names,
        desc="Tokenize test",
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    steps_per_epoch = max(
        1,
        len(tokenized_train)
        // (BATCH_SIZE * GRADIENT_ACCUMULATION_STEPS),
    )
    total_steps = steps_per_epoch * NUM_EPOCHS

    training_args = Seq2SeqTrainingArguments(
        output_dir=str(OUTPUT_DIR / "checkpoints"),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=EVAL_BATCH_SIZE,
        gradient_accumulation_steps=GRADIENT_ACCUMULATION_STEPS,
        learning_rate=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
        warmup_ratio=WARMUP_RATIO,
        eval_strategy=EVAL_STRATEGY,
        save_strategy=SAVE_STRATEGY,
        logging_steps=LOGGING_STEPS,
        logging_dir=str(LOGS_DIR),
        save_total_limit=SAVE_TOTAL_LIMIT,
        load_best_model_at_end=LOAD_BEST_MODEL_AT_END,
        metric_for_best_model=METRIC_FOR_BEST_MODEL,
        greater_is_better=GREATER_IS_BETTER,
        predict_with_generate=True,
        generation_max_length=MAX_TARGET_LENGTH,
        fp16=FP16 and device == "cuda",
        dataloader_num_workers=0,
        disable_tqdm=True,
        report_to=[],
        seed=RANDOM_SEED,
    )

    progress_callback = TrainingProgressCallback(
        total_steps=total_steps,
        num_epochs=NUM_EPOCHS,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        tokenizer=tokenizer,
        data_collator=data_collator,
        callbacks=[progress_callback],
    )

    print("\n[2/4] Training model...")
    logger.info("Starting training with model %s", MODEL_NAME)
    logger.info(
        "Training plan: %d epochs, %d steps/epoch, %d total steps",
        NUM_EPOCHS,
        steps_per_epoch,
        total_steps,
    )
    train_result = trainer.train()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    trainer.save_model(str(OUTPUT_DIR))
    tokenizer.save_pretrained(str(OUTPUT_DIR))

    train_metrics = train_result.metrics
    train_metrics_path = LOGS_DIR / "train_metrics.json"
    with train_metrics_path.open("w", encoding="utf-8") as file:
        json.dump(train_metrics, file, indent=2)

    logger.info("Evaluating on test set...")
    print("\n[3/4] Evaluating on test set...")
    eval_progress = PhaseProgress(total=3, desc="Evaluate")
    eval_progress.update()
    test_metrics = run_test_evaluation(trainer, tokenized_test, test_dataset, tokenizer)
    eval_progress.update()
    metrics_path = save_metrics(test_metrics, OUTPUT_DIR / "evaluation_metrics.json")
    eval_progress.update()
    eval_progress.close()

    split_info = {
        "train_size": len(train_dataset),
        "val_size": len(val_dataset),
        "test_size": len(test_dataset),
        "model_name": MODEL_NAME,
        "epochs": NUM_EPOCHS,
        "best_checkpoint": str(OUTPUT_DIR),
    }
    with (OUTPUT_DIR / "training_summary.json").open("w", encoding="utf-8") as file:
        json.dump(
            {"split": split_info, "train_metrics": train_metrics, "test_metrics": test_metrics},
            file,
            indent=2,
        )

    logger.info("Test metrics: %s", test_metrics)
    logger.info("Metrics saved to %s", metrics_path)

    print("\n[4/4] Exporting ONNX model...")
    export_progress = PhaseProgress(total=2, desc="ONNX export")
    export_progress.update()
    export_to_onnx(model, tokenizer, OUTPUT_DIR / "onnx")
    export_progress.update()
    export_progress.close()

    # Quick sanity example
    example_input = TASK_PREFIX + "Can you please explain AI in detail?"
    inputs = tokenizer(example_input, return_tensors="pt", truncation=True)
    if device == "mps":
        inputs = {k: v.to("mps") for k, v in inputs.items()}
        model = model.to("mps")
    elif device == "cuda":
        inputs = {k: v.to("cuda") for k, v in inputs.items()}
        model = model.to("cuda")

    with torch.no_grad():
        output_ids = model.generate(**inputs, max_new_tokens=MAX_TARGET_LENGTH)
    example_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    logger.info('Example output: "%s"', example_output)


if __name__ == "__main__":
    main()
