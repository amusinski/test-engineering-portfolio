"""
base_page.py — Base Page Object with shared helpers.

Every page object in this project inherits from BasePage.
"""

from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class BasePage:
    """
    Base class for all Page Object Model (POM) classes.

    Provides:
    - Navigation helpers
    - Common assertion wrappers
    - Retry-aware wait utilities
    """

    def __init__(self, page: Page) -> None:
        self._page = page

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def navigate(self, path: str = "/") -> None:
        """Navigate to *path* relative to BASE_URL."""
        self._page.goto(path)

    def reload(self) -> None:
        self._page.reload()

    @property
    def url(self) -> str:
        return self._page.url

    @property
    def title(self) -> str:
        return self._page.title()

    # ------------------------------------------------------------------
    # Common interaction wrappers
    # ------------------------------------------------------------------

    def fill(self, locator: Locator, value: str) -> None:
        """Clear then fill *locator* with *value*."""
        locator.clear()
        locator.fill(value)

    def click(self, locator: Locator) -> None:
        locator.click()

    def select_option(self, locator: Locator, value: str) -> None:
        locator.select_option(value)

    # ------------------------------------------------------------------
    # Wait / assertion helpers
    # ------------------------------------------------------------------

    def wait_for_url(self, pattern: str, timeout: int = 10_000) -> None:
        self._page.wait_for_url(pattern, timeout=timeout)

    def expect_visible(self, locator: Locator, timeout: int = 10_000) -> None:
        expect(locator).to_be_visible(timeout=timeout)

    def expect_hidden(self, locator: Locator, timeout: int = 10_000) -> None:
        expect(locator).to_be_hidden(timeout=timeout)

    def expect_text(self, locator: Locator, text: str, timeout: int = 10_000) -> None:
        expect(locator).to_have_text(text, timeout=timeout)

    def expect_url_contains(self, substring: str, timeout: int = 10_000) -> None:
        expect(self._page).to_have_url(f"*{substring}*", timeout=timeout)

    # ------------------------------------------------------------------
    # Screenshot helper (useful in hooks or teardown)
    # ------------------------------------------------------------------

    def screenshot(self, name: str) -> bytes:
        return self._page.screenshot(path=f"screenshots/{name}.png", full_page=True)
