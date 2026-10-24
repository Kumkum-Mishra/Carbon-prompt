"""Main orchestration layer for prompt analysis."""

import logging
from datetime import datetime, timezone

from analyzer.config import LOG_FULL_PROMPT
from analyzer.prompt_type_classifier import classify_prompt_type
from analyzer.schemas import AnalysisResult, ErrorResponse, SuccessResponse
from analyzer.task_classifier import classify_task
from analyzer.tokenizer import TokenizerError, count_tokens
from analyzer.utils import clean_prompt, count_words

logger = logging.getLogger(__name__)


class PromptAnalyzer:
    """Analyzes raw prompts and returns structured metadata."""

    def analyze(self, raw_prompt: str) -> SuccessResponse | ErrorResponse:
        cleaned = clean_prompt(raw_prompt)

        try:
            token_count = count_tokens(cleaned)
        except TokenizerError as exc:
            logger.error("Tokenizer error: %s", exc)
            return ErrorResponse(message="Unable to calculate tokens.")

        task_type = classify_task(cleaned)
        prompt_type = classify_prompt_type(cleaned)
        character_count = len(cleaned)
        word_count = count_words(cleaned)

        self._log_analysis(
            prompt_length=character_count,
            token_count=token_count,
            task_type=task_type,
            prompt_type=prompt_type,
            cleaned_prompt=cleaned,
        )

        return SuccessResponse(
            analysis=AnalysisResult(
                prompt=cleaned,
                prompt_type=prompt_type,
                task_type=task_type,
                category=task_type,
                token_count=token_count,
                character_count=character_count,
                word_count=word_count,
            )
        )

    def _log_analysis(
        self,
        *,
        prompt_length: int,
        token_count: int,
        task_type: str,
        prompt_type: str,
        cleaned_prompt: str,
    ) -> None:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt_length": prompt_length,
            "token_count": token_count,
            "task_type": task_type,
            "prompt_type": prompt_type,
        }
        if LOG_FULL_PROMPT:
            log_data["prompt"] = cleaned_prompt

        logger.info("Prompt analysis completed: %s", log_data)
