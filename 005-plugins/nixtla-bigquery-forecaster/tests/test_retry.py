"""Tests for retry_on_transient — exponential backoff for BigQuery calls."""

from __future__ import annotations

import time

import pytest
from src.retry import retry_on_transient

# Build a fake transient exception class — we patch the resolver to return
# this class so we can test retry behavior without depending on
# google-cloud-bigquery being installed at test time.


class _FakeTransient(Exception):
    """Stand-in for google.api_core.exceptions.ServiceUnavailable etc."""


class _FakePermanent(Exception):
    """Stand-in for any non-retryable exception."""


@pytest.fixture(autouse=True)
def patch_transient_types(monkeypatch):
    """Force retry_on_transient to treat _FakeTransient as the retryable type."""
    monkeypatch.setattr(
        "src.retry._transient_exception_types",
        lambda: (_FakeTransient,),
    )


@pytest.fixture(autouse=True)
def fast_sleep(monkeypatch):
    """Skip real sleeps — tests should run quickly."""
    monkeypatch.setattr(time, "sleep", lambda _s: None)


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestSuccess:
    def test_succeeds_on_first_call(self):
        calls = []

        @retry_on_transient(max_attempts=3)
        def fn():
            calls.append(1)
            return "ok"

        assert fn() == "ok"
        assert len(calls) == 1

    def test_succeeds_on_second_attempt(self):
        calls = []

        @retry_on_transient(max_attempts=3, initial_backoff_s=0.01, jitter=0)
        def fn():
            calls.append(1)
            if len(calls) < 2:
                raise _FakeTransient("flake")
            return "ok"

        assert fn() == "ok"
        assert len(calls) == 2

    def test_succeeds_on_last_attempt(self):
        calls = []

        @retry_on_transient(max_attempts=4, initial_backoff_s=0.01, jitter=0)
        def fn():
            calls.append(1)
            if len(calls) < 4:
                raise _FakeTransient("flake")
            return "ok"

        assert fn() == "ok"
        assert len(calls) == 4


# ---------------------------------------------------------------------------
# Exhaustion
# ---------------------------------------------------------------------------


class TestExhaustion:
    def test_reraises_after_max_attempts(self):
        calls = []

        @retry_on_transient(max_attempts=3, initial_backoff_s=0.01, jitter=0)
        def fn():
            calls.append(1)
            raise _FakeTransient("permanent flake")

        with pytest.raises(_FakeTransient, match="permanent flake"):
            fn()
        assert len(calls) == 3


# ---------------------------------------------------------------------------
# Non-transient exceptions are NOT retried
# ---------------------------------------------------------------------------


class TestNonTransient:
    def test_permanent_exception_raised_immediately(self):
        calls = []

        @retry_on_transient(max_attempts=5, initial_backoff_s=0.01, jitter=0)
        def fn():
            calls.append(1)
            raise _FakePermanent("not retryable")

        with pytest.raises(_FakePermanent):
            fn()
        # Should have been tried exactly once.
        assert len(calls) == 1


# ---------------------------------------------------------------------------
# Backoff values (no real sleeping — verify the cap math)
# ---------------------------------------------------------------------------


class TestBackoffMath:
    def test_backoff_capped_by_max_backoff_s(self, monkeypatch):
        """Backoff = min(initial * 2^attempt, max_backoff_s); jitter is fractional."""
        sleeps: list[float] = []
        monkeypatch.setattr(time, "sleep", lambda s: sleeps.append(s))

        @retry_on_transient(
            max_attempts=4,
            initial_backoff_s=10.0,
            max_backoff_s=15.0,
            jitter=0,
        )
        def fn():
            raise _FakeTransient("flake")

        with pytest.raises(_FakeTransient):
            fn()

        # Attempt 0 fails → sleep 10. Attempt 1 fails → sleep min(20, 15) = 15.
        # Attempt 2 fails → sleep min(40, 15) = 15. Attempt 3 fails → no sleep
        # (no further attempt to retry).
        assert sleeps == [10.0, 15.0, 15.0]
