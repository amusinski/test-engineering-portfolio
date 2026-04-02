"""
helpers.py — Shared utility functions used across the test suite.
"""

from __future__ import annotations

import re
import time
import uuid
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any


# ---------------------------------------------------------------------------
# Unique data generators
# ---------------------------------------------------------------------------


def unique_email(prefix: str = "test") -> str:
    """Return a unique email address suitable for test user creation."""
    return f"{prefix}+{uuid.uuid4().hex[:8]}@example.com"


def unique_username(prefix: str = "user") -> str:
    """Return a unique username."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


# ---------------------------------------------------------------------------
# Text utilities
# ---------------------------------------------------------------------------


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace into a single space and strip edges."""
    return re.sub(r"\s+", " ", text).strip()


def extract_numbers(text: str) -> list[int]:
    """Return all integers found in *text*."""
    return [int(n) for n in re.findall(r"\d+", text)]


# ---------------------------------------------------------------------------
# Retry helper
# ---------------------------------------------------------------------------


def retry(
    func,  # noqa: ANN001
    *,
    attempts: int = 3,
    delay_s: float = 1.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Any:
    """
    Call *func* up to *attempts* times, sleeping *delay_s* seconds between tries.

    Raises the last exception if all attempts fail.

    Example::

        result = retry(lambda: unstable_api_call(), attempts=5, delay_s=2)
    """
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            return func()
        except exceptions as exc:
            last_exc = exc
            if attempt < attempts - 1:
                time.sleep(delay_s)
    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Timing context manager
# ---------------------------------------------------------------------------


@contextmanager
def measure_time() -> Generator[dict[str, float], None, None]:
    """
    Context manager that records wall-clock duration.

    Example::

        with measure_time() as timing:
            page.click(button)
        assert timing["elapsed_s"] < 2.0
    """
    result: dict[str, float] = {}
    start = time.perf_counter()
    yield result
    result["elapsed_s"] = time.perf_counter() - start


# ---------------------------------------------------------------------------
# Playwright-specific helpers
# ---------------------------------------------------------------------------


def wait_for_network_idle(page, timeout_ms: int = 5_000) -> None:  # noqa: ANN001
    """Wait until there are no in-flight network requests."""
    page.wait_for_load_state("networkidle", timeout=timeout_ms)


def get_local_storage(page, key: str) -> str | None:  # noqa: ANN001
    """Read a value from the page's localStorage."""
    return page.evaluate("(key) => window.localStorage.getItem(key)", key)


def set_local_storage(page, key: str, value: str) -> None:  # noqa: ANN001
    """Write a value to the page's localStorage."""
    page.evaluate("([key, value]) => window.localStorage.setItem(key, value)", [key, value])


def dismiss_cookie_banner(page) -> None:  # noqa: ANN001
    """
    Dismiss a cookie consent banner if present.

    Silently does nothing if no banner is found.
    """
    banner = page.locator("[data-testid='cookie-banner']")
    if banner.is_visible(timeout=2_000):
        page.get_by_role("button", name=re.compile(r"accept|agree|ok", re.IGNORECASE)).first.click()
        banner.wait_for(state="hidden", timeout=3_000)
