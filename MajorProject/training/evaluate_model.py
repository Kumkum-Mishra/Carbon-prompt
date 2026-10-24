"""Evaluation metrics for the prompt optimization model."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from bert_score import score as bert_score
from rouge_score import rouge_scorer
from sacrebleu.metrics import BLEU
from transformers import PreTrainedTokenizerBase

from training.config import OUTPUT_DIR


def count_tokens(text: str, tokenizer: PreTrainedTokenizerBase) -> int:
    return len(tokenizer.encode(text, add_special_tokens=False))


def compute_metrics(
    predictions: list[str],
    references: list[str],
    sources: list[str],
    tokenizer: PreTrainedTokenizerBase,
) -> dict[str, float]:
    """Compute BLEU, ROUGE, BERTScore, Exact Match, and token reduction."""
    predictions = [p.strip() for p in predictions]
    references = [r.strip() for r in references]
    sources = [s.strip() for s in sources]

    bleu = BLEU()
    bleu_score = bleu.corpus_score(predictions, [references]).score

    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    rouge1, rouge2, rouge_l = [], [], []
    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        rouge1.append(scores["rouge1"].fmeasure)
        rouge2.append(scores["rouge2"].fmeasure)
        rouge_l.append(scores["rougeL"].fmeasure)

    exact_match = sum(
        1 for pred, ref in zip(predictions, references) if pred.lower() == ref.lower()
    ) / len(predictions)

    _, _, f1 = bert_score(
        predictions,
        references,
        lang="en",
        rescale_with_baseline=True,
        verbose=False,
    )
    bertscore_f1 = float(f1.mean())

    reductions = []
    for source, pred in zip(sources, predictions):
        source_tokens = count_tokens(source, tokenizer)
        pred_tokens = count_tokens(pred, tokenizer)
        if source_tokens > 0:
            reductions.append((source_tokens - pred_tokens) / source_tokens * 100)
        else:
            reductions.append(0.0)

    return {
        "bleu": round(float(bleu_score), 4),
        "rouge1": round(float(np.mean(rouge1)), 4),
        "rouge2": round(float(np.mean(rouge2)), 4),
        "rougeL": round(float(np.mean(rouge_l)), 4),
        "bertscore_f1": round(bertscore_f1, 4),
        "exact_match": round(float(exact_match), 4),
        "avg_token_reduction_percent": round(float(np.mean(reductions)), 4),
    }


def save_metrics(metrics: dict, path: Path | None = None) -> Path:
    output_path = path or (OUTPUT_DIR / "evaluation_metrics.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2)
    return output_path
