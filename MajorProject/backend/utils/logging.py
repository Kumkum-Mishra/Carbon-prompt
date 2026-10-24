"""Logging configuration for the API gateway."""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import IS_PRODUCTION, LOG_DIR, LOG_FULL_PROMPT, LOG_LEVEL, LOG_TO_FILE


def setup_logging() -> None:
    """Configure structured logging to stdout and optional log files."""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(log_level)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    root_logger.addHandler(stdout_handler)

    if LOG_TO_FILE:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            LOG_DIR / "greenprompt.log",
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    if IS_PRODUCTION and LOG_FULL_PROMPT:
        logging.getLogger(__name__).warning(
            "LOG_FULL_PROMPT is enabled in production; disable for privacy."
        )


def log_request_event(
    *,
    endpoint: str,
    method: str,
    status_code: int,
    processing_time_ms: float,
    task_type: str | None = None,
    token_count: int | None = None,
    carbon_score: float | None = None,
    recommended_model: str | None = None,
) -> None:
    """Log a structured request summary without sensitive data."""
    logger = logging.getLogger("gateway.requests")
    payload = {
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "processing_time_ms": round(processing_time_ms, 2),
    }
    if task_type is not None:
        payload["task_type"] = task_type
    if token_count is not None:
        payload["token_count"] = token_count
    if carbon_score is not None:
        payload["carbon_score"] = carbon_score
    if recommended_model is not None:
        payload["recommended_model"] = recommended_model
    logger.info("Request completed: %s", payload)
