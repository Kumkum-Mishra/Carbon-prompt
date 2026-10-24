#!/usr/bin/env python3
"""Finish post-training steps using the already-saved model (no retraining).

Runs:
1. Quick live prompt-optimization demos
2. Fast test-set evaluation on a sample (default 100)
3. Writes evaluation_metrics.json + training_summary.json
4. Attempts ONNX export
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from training.config import (  # noqa: E402
    LOGS_DIR,
    MAX_TARGET_LENGTH,
    MODEL_NAME,
    NUM_EPOCHS,
    OUTPUT_DIR,
    TASK_PREFIX,
)
from training.evaluate_model import compute_metrics, save_metrics  # noqa: E402
from training.train_prompt_optimizer import (  # noqa: E402
    export_to_onnx,
    load_and_split_dataset,
    setup_logging,
)

logger = logging.getLogger(__name__)

DEMO_PROMPTS = [
    "Can you please explain in great detail, with many examples, how neural networks work and also discuss all their applications?",
    "Write CNN code using PyTorch.",
    "Act as a senior backend engineer and carefully review this API design for scalability issues.",
    "Could you please summarize the key findings of this research paper in three bullet points?",
    "I want you to help me understand what machine learning is and how it works in a very detailed way with lots of explanations.",
]


def pick_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def optimize_prompt(model, tokenizer, prompt: str, device: str) -> str:
    text = TASK_PREFIX + prompt
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=128,
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=MAX_TARGET_LENGTH,
            num_beams=4,
            early_stopping=True,
        )
    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()


def count_words(text: str) -> int:
    return len(text.split())


def run_demos(model, tokenizer, device: str) -> list[dict]:
    print("\n=== Quick optimization demos ===")
    results = []
    for i, prompt in enumerate(DEMO_PROMPTS, start=1):
        t0 = time.time()
        optimized = optimize_prompt(model, tokenizer, prompt, device)
        elapsed = time.time() - t0
        before = count_words(prompt)
        after = count_words(optimized)
        reduction = ((before - after) / before * 100) if before else 0.0
        row = {
            "original": prompt,
            "optimized": optimized,
            "words_before": before,
            "words_after": after,
            "word_reduction_percent": round(reduction, 1),
            "seconds": round(elapsed, 2),
        }
        results.append(row)
        print(f"\n[{i}/{len(DEMO_PROMPTS)}]")
        print(f"ORIGINAL ({before} words): {prompt}")
        print(f"OPTIMIZED ({after} words, {reduction:.1f}% shorter, {elapsed:.2f}s): {optimized}")
    return results


def run_fast_test_eval(model, tokenizer, device: str, sample_size: int) -> dict:
    print(f"\n=== Fast test evaluation (n={sample_size}) ===")
    _, _, test_dataset = load_and_split_dataset()
    n = min(sample_size, len(test_dataset))
    subset = test_dataset.select(range(n))

    preds: list[str] = []
    sources = list(subset["original_prompt"])
    references = list(subset["optimized_prompt"])

    t0 = time.time()
    for i, source in enumerate(sources, start=1):
        preds.append(optimize_prompt(model, tokenizer, source, device))
        if i % 10 == 0 or i == n:
            print(f"  evaluated {i}/{n}...")
    elapsed = time.time() - t0

    metrics = compute_metrics(preds, references, sources, tokenizer)
    metrics["eval_samples"] = n
    metrics["eval_seconds"] = round(elapsed, 2)
    metrics["eval_note"] = (
        f"Fast sample evaluation on {n}/{len(test_dataset)} held-out test prompts"
    )
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-size", type=int, default=50)
    parser.add_argument("--skip-onnx", action="store_true")
    parser.add_argument("--skip-eval", action="store_true")
    args = parser.parse_args()

    setup_logging()
    device = pick_device()
    model_dir = OUTPUT_DIR
    if not (model_dir / "model.safetensors").exists() and not (model_dir / "pytorch_model.bin").exists():
        raise FileNotFoundError(f"Saved model not found in {model_dir}")

    print(f"Loading saved model from: {model_dir}")
    print(f"Device: {device}")
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForSeq2SeqLM.from_pretrained(str(model_dir))
    model.to(device)
    model.eval()

    demos = run_demos(model, tokenizer, device)
    demos_path = model_dir / "demo_optimizations.json"
    with demos_path.open("w", encoding="utf-8") as file:
        json.dump(demos, file, indent=2)
    print(f"\nDemo results saved to {demos_path}")

    shorter = sum(1 for d in demos if d["words_after"] < d["words_before"])
    changed = sum(1 for d in demos if d["optimized"].strip().lower() != d["original"].strip().lower())
    print("\n=== Verdict ===")
    print(f"Prompts shortened: {shorter}/{len(demos)}")
    print(f"Prompts changed:   {changed}/{len(demos)}")
    if shorter >= 3:
        print("Result: YES — the model is optimizing prompts (making them shorter while keeping intent).")
    elif changed >= 3:
        print("Result: PARTIAL — the model rewrites prompts, but shortening is inconsistent.")
    else:
        print("Result: WEAK — outputs look too similar to inputs; check training data / inference.")

    test_metrics = {}
    if not args.skip_eval:
        test_metrics = run_fast_test_eval(model, tokenizer, device, args.sample_size)
        metrics_path = save_metrics(test_metrics, model_dir / "evaluation_metrics.json")
        print(f"\nTest metrics: {json.dumps(test_metrics, indent=2)}")
        print(f"Saved to {metrics_path}")

    train_metrics = {}
    train_metrics_path = LOGS_DIR / "train_metrics.json"
    if train_metrics_path.exists():
        with train_metrics_path.open(encoding="utf-8") as file:
            train_metrics = json.load(file)

    summary = {
        "model_path": str(model_dir),
        "base_model": MODEL_NAME,
        "epochs": NUM_EPOCHS,
        "train_metrics": train_metrics,
        "test_metrics": test_metrics,
        "demo_summary": {
            "n": len(demos),
            "shortened": shorter,
            "changed": changed,
            "avg_word_reduction_percent": round(
                sum(d["word_reduction_percent"] for d in demos) / max(len(demos), 1),
                2,
            ),
        },
    }
    summary_path = model_dir / "training_summary.json"
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
    print(f"Training summary saved to {summary_path}")

    if not args.skip_onnx:
        print("\n=== ONNX export ===")
        ok = export_to_onnx(model, tokenizer, model_dir / "onnx")
        print("ONNX export:", "ok" if ok else "skipped/failed")

    print("\nDone. Saved model directory:")
    print(f"  {model_dir}")


if __name__ == "__main__":
    main()
