"""Shared error response utilities."""

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: str | None = None


def build_error_response(
    message: str,
    *,
    status_code: int = 400,
    details: str | None = None,
) -> JSONResponse:
    """Return a standardized JSON error response."""
    return JSONResponse(
        status_code=status_code,
        content=ErrorResponse(message=message, details=details).model_dump(),
    )
