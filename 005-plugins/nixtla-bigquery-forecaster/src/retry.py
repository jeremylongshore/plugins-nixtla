"""Retry helpers for BigQuery API calls.

BigQuery's Python SDK retries some transient errors at the transport layer,
but the high-level ``client.query()`` / ``client.load_table_from_dataframe()``
calls don't retry on application-visible failures (e.g., 503 / quota
exceeded burst). This module wraps the call sites with explicit
exponential backoff so production runs survive transient hiccups.
"""

from __future__ import annotations

import functools
import logging
import random
import time
from typing import Callable, Tuple, Type, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


# Exception types we retry. Imported lazily because google-cloud-bigquery
# may not be installed in lightweight test environments.
def _transient_exception_types() -> Tuple[Type[BaseException], ...]:
    types: list[Type[BaseException]] = []
    try:
        from google.api_core import exceptions as gax_exc

        types.extend(
            [
                gax_exc.ServiceUnavailable,
                gax_exc.TooManyRequests,
                gax_exc.InternalServerError,
                gax_exc.GatewayTimeout,
                gax_exc.DeadlineExceeded,
            ]
        )
    except ImportError:
        # Fall through with empty tuple — caller will get the original error.
        logger.debug("google.api_core not importable; retry decorator is a no-op")
    return tuple(types)


def retry_on_transient(
    max_attempts: int = 5,
    initial_backoff_s: float = 1.0,
    max_backoff_s: float = 30.0,
    jitter: float = 0.5,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator: retry on transient BigQuery / GCP errors with backoff.

    Backoff: ``initial_backoff_s * 2**attempt``, capped at ``max_backoff_s``,
    plus uniform jitter ``[-jitter*backoff, +jitter*backoff]``.

    Args:
        max_attempts: Total attempts (including the first). Default 5.
        initial_backoff_s: Base backoff for the first retry. Default 1s.
        max_backoff_s: Cap for any single backoff. Default 30s.
        jitter: Fraction of backoff to add as random jitter [0..1]. Default 0.5.

    Re-raises the last exception if all attempts fail. Non-transient
    exceptions are NOT retried.
    """

    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs) -> T:
            transient = _transient_exception_types()
            last_exc: BaseException | None = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except BaseException as exc:  # noqa: BLE001 — we re-raise
                    if not transient or not isinstance(exc, transient):
                        raise
                    last_exc = exc
                    if attempt == max_attempts - 1:
                        logger.error(
                            "BigQuery call failed after %d attempts: %s",
                            max_attempts,
                            exc,
                        )
                        raise
                    backoff = min(initial_backoff_s * (2**attempt), max_backoff_s)
                    delta = random.uniform(-jitter * backoff, jitter * backoff)
                    sleep_s = max(0.0, backoff + delta)
                    logger.warning(
                        "BigQuery call attempt %d/%d failed (%s); retrying in %.2fs",
                        attempt + 1,
                        max_attempts,
                        type(exc).__name__,
                        sleep_s,
                    )
                    time.sleep(sleep_s)
            # Defensive — loop should have either returned or raised.
            assert last_exc is not None
            raise last_exc

        return wrapper

    return decorator
