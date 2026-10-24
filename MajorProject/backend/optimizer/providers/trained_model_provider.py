"""Local trained FLAN-T5 provider for prompt optimization."""

from __future__ import annotations

import logging
from pathlib import Path

from optimizer.config import (
    OPTIMIZER_MAX_NEW_TOKENS,
    OPTIMIZER_NUM_BEAMS,
    OPTIMIZER_NUM_CANDIDATES,
    OPTIMIZER_TASK_PREFIX,
    TRAINED_MODEL_DEVICE,
    TRAINED_MODEL_PATH,
)
from optimizer.providers.base import (
    BaseLLMProvider,
    LLMOptimizationError,
    LLMProviderUnavailableError,
)

logger = logging.getLogger(__name__)


class TrainedModelProvider(BaseLLMProvider):
    """Uses the locally fine-tuned FLAN-T5 prompt optimizer."""

    def __init__(self, model_path: Path | None = None) -> None:
        self._model_path = (model_path or TRAINED_MODEL_PATH).resolve()
        self._tokenizer = None
        self._model = None
        self._device = "cpu"

    @property
    def provider_name(self) -> str:
        return "trained_model"

    @property
    def model_name(self) -> str:
        return str(self._model_path)

    def optimize(self, prompt: str, system_prompt: str) -> str:
        candidates = self.optimize_candidates(prompt, system_prompt, num_candidates=1)
        return candidates[0] if candidates else prompt.strip()

    def optimize_candidates(
        self,
        prompt: str,
        system_prompt: str,
        num_candidates: int = OPTIMIZER_NUM_CANDIDATES,
    ) -> list[str]:
        self._ensure_loaded()
        try:
            import torch

            text = OPTIMIZER_TASK_PREFIX + prompt.strip()
            inputs = self._tokenizer(  # type: ignore[operator]
                text,
                return_tensors="pt",
                truncation=True,
                max_length=128,
            )
            inputs = {key: value.to(self._device) for key, value in inputs.items()}

            # Beam search returns top-K candidates; HF requires returns <= beams.
            returns = max(1, min(num_candidates, OPTIMIZER_NUM_CANDIDATES))
            beams = max(returns, OPTIMIZER_NUM_BEAMS)
            with torch.no_grad():
                output_ids = self._model.generate(  # type: ignore[union-attr]
                    **inputs,
                    max_new_tokens=OPTIMIZER_MAX_NEW_TOKENS,
                    num_beams=beams,
                    num_return_sequences=returns,
                    early_stopping=True,
                    no_repeat_ngram_size=3,
                )

            decoded = self._tokenizer.batch_decode(  # type: ignore[operator]
                output_ids,
                skip_special_tokens=True,
            )
            unique: list[str] = []
            seen: set[str] = set()
            for candidate in decoded:
                cleaned = " ".join(candidate.strip().split())
                key = cleaned.lower()
                if cleaned and key not in seen:
                    unique.append(cleaned)
                    seen.add(key)
            return unique or [prompt.strip()]
        except Exception as exc:
            logger.exception("Local trained model optimization failed")
            raise LLMOptimizationError(str(exc)) from exc

    def _ensure_loaded(self) -> None:
        if self._model is not None and self._tokenizer is not None:
            return
        if not self._model_path.exists():
            raise LLMProviderUnavailableError(
                f"Trained model path does not exist: {self._model_path}"
            )
        if not (self._model_path / "config.json").exists():
            raise LLMProviderUnavailableError(
                f"Trained model config missing: {self._model_path}"
            )

        try:
            import torch
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        except Exception as exc:
            raise LLMProviderUnavailableError(
                "Install torch, transformers, sentencepiece, and safetensors "
                "to use LLM_PROVIDER=trained_model."
            ) from exc

        if TRAINED_MODEL_DEVICE == "auto":
            if torch.cuda.is_available():
                self._device = "cuda"
            elif torch.backends.mps.is_available():
                self._device = "mps"
            else:
                self._device = "cpu"
        else:
            self._device = TRAINED_MODEL_DEVICE

        logger.info("Loading trained prompt optimizer from %s", self._model_path)
        self._tokenizer = AutoTokenizer.from_pretrained(str(self._model_path))
        self._model = AutoModelForSeq2SeqLM.from_pretrained(str(self._model_path))
        self._model.to(self._device)
        self._model.eval()
