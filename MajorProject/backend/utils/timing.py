"""Request timing helpers."""

import time
from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def measure_time() -> Generator[dict[str, float], None, None]:
    """Measure elapsed time in milliseconds."""
    result = {"elapsed_ms": 0.0}
    start = time.perf_counter()
    try:
        yield result
    finally:
        result["elapsed_ms"] = (time.perf_counter() - start) * 1000
