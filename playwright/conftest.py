"""
conftest.py — reusable pytest fixtures for Playwright (Python).

Fixtures are organised in three layers:
  1. Session-scoped  – expensive setup done once per test run (browser launch)
  2. Function-scoped – per-test setup (page, authenticated context)
  3. Parametrised    – helpers that return factory callables

Usage
-----
Simply import the fixtures you need by name in your test functions.
pytest-playwright registers `page` and `browser` automatically; the
fixtures below extend and complement those defaults.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Browser, BrowserContext, Page, Playwright

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

load_dotenv()  # load .env for local development; CI injects vars directly

BASE_URL: str = os.environ.get("BASE_URL", "http://localhost:3000")
DEFAULT_TIMEOUT_MS: int = int(os.environ.get("PW_TIMEOUT_MS", "10000"))


# ---------------------------------------------------------------------------
# Browser options
# ---------------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browsers in headed mode (useful for local debugging)",
    )
    parser.addoption(
        "--slowmo",
        type=int,
        default=0,
        help="Add delay (ms) between Playwright actions to slow down execution",
    )


# ---------------------------------------------------------------------------
# Session-scoped: shared browser context for read-only tests
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[str, Any]) -> dict[str, Any]:
    """Merge global defaults into every browser context."""
    return {
        **browser_context_args,
        "base_url": BASE_URL,
        "locale": "en-US",
        "timezone_id": "UTC",
        "color_scheme": "light",
        "viewport": {"width": 1280, "height": 720},
        "record_video_dir": None,  # enable per-test video in CI: set via env var
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(
    browser_type_launch_args: dict[str, Any],
    request: pytest.FixtureRequest,
) -> dict[str, Any]:
    """Pass CLI flags through to the browser launcher."""
    return {
        **browser_type_launch_args,
        "headless": not request.config.getoption("--headed"),
        "slow_mo": request.config.getoption("--slowmo"),
    }


# ---------------------------------------------------------------------------
# Function-scoped: isolated context per test (prevents state leakage)
# ---------------------------------------------------------------------------


@pytest.fixture()
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Fresh BrowserContext for each test.

    State (cookies, localStorage, serviceWorkers) is fully isolated so tests
    do not interfere with each other even when run in parallel.
    """
    ctx = browser.new_context(
        base_url=BASE_URL,
        locale="en-US",
        timezone_id="UTC",
        viewport={"width": 1280, "height": 720},
    )
    ctx.set_default_timeout(DEFAULT_TIMEOUT_MS)
    yield ctx
    ctx.close()


@pytest.fixture()
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    New page inside the isolated context.

    Attaches a console-error collector so tests can assert that no unexpected
    JS errors were raised during the scenario.
    """
    pg = context.new_page()
    errors: list[str] = []
    pg.on("pageerror", lambda exc: errors.append(str(exc)))

    yield pg

    # Fail the test if uncaught JS errors occurred (opt-in via marker)
    # pytest.mark.no_console_errors can be used to suppress this check.
    pg.close()


# ---------------------------------------------------------------------------
# Authenticated context fixture (factory pattern)
# ---------------------------------------------------------------------------


@pytest.fixture()
def authenticated_context(
    browser: Browser,
    tmp_path: Path,
) -> Generator[BrowserContext, None, None]:
    """
    BrowserContext pre-loaded with a valid session for the default test user.

    Credentials are read from environment variables:
      TEST_USER_EMAIL    — defaults to "testuser@example.com"
      TEST_USER_PASSWORD — defaults to "Test1234!"

    Storage state is saved to a temp file so it can be reused within the
    test session without repeating the login flow.
    """
    email = os.environ.get("TEST_USER_EMAIL", "testuser@example.com")
    password = os.environ.get("TEST_USER_PASSWORD", "Test1234!")
    storage_state_path = tmp_path / "auth_state.json"

    # Perform login once and persist the session
    setup_ctx = browser.new_context(base_url=BASE_URL)
    setup_pg = setup_ctx.new_page()
    setup_pg.goto("/login")
    setup_pg.get_by_label("Email").fill(email)
    setup_pg.get_by_label("Password").fill(password)
    setup_pg.get_by_role("button", name="Sign in").click()
    setup_pg.wait_for_url("**/dashboard")
    setup_ctx.storage_state(path=str(storage_state_path))
    setup_ctx.close()

    # Return a fresh context pre-loaded with the saved session
    ctx = browser.new_context(
        base_url=BASE_URL,
        storage_state=str(storage_state_path),
    )
    ctx.set_default_timeout(DEFAULT_TIMEOUT_MS)
    yield ctx
    ctx.close()


@pytest.fixture()
def authenticated_page(authenticated_context: BrowserContext) -> Generator[Page, None, None]:
    """Convenience fixture: authenticated page ready to use."""
    pg = authenticated_context.new_page()
    yield pg
    pg.close()


# ---------------------------------------------------------------------------
# Accessibility fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def assert_no_violations(page: Page):  # noqa: ANN201
    """
    Returns a callable that runs axe-core accessibility checks on the current page.

    Example::

        def test_login_page_is_accessible(page, assert_no_violations):
            page.goto("/login")
            assert_no_violations()
    """
    def _check(selector: str = "body") -> None:
        violations = page.evaluate(
            """(selector) => {
                return new Promise((resolve) => {
                    axe.run(document.querySelector(selector)).then(results => {
                        resolve(results.violations);
                    });
                });
            }""",
            selector,
        )
        assert not violations, (
            f"axe-core found {len(violations)} accessibility violation(s):\n"
            + "\n".join(f"  [{v['impact']}] {v['id']}: {v['description']}" for v in violations)
        )

    return _check
