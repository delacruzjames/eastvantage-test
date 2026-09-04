"""HTTP middleware."""

import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response

from app.logging_config import get_logger

logger = get_logger(__name__)


async def log_requests(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    """Log one line per request with its status code and duration."""
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = (time.perf_counter() - started) * 1000
        logger.exception(
            "%s %s failed after %.1fms",
            request.method,
            request.url.path,
            elapsed_ms,
        )
        raise

    elapsed_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "%s %s -> %s in %.1fms",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response
