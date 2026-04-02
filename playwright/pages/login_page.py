"""
login_page.py — Page Object for the login screen.
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates all interactions with the /login page."""

    PATH = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Locators — using accessible roles/labels for resilience
        self.email_input = page.get_by_label("Email")
        self.password_input = page.get_by_label("Password")
        self.submit_button = page.get_by_role("button", name="Sign in")
        self.error_banner = page.get_by_role("alert")
        self.forgot_password_link = page.get_by_role("link", name="Forgot password")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "LoginPage":
        self.navigate(self.PATH)
        return self

    def login(self, email: str, password: str) -> None:
        """Fill credentials and submit the form."""
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.submit_button)

    def login_and_wait(self, email: str, password: str, redirect_pattern: str = "**/dashboard") -> None:
        """Login and wait for successful redirect."""
        self.login(email, password)
        self.wait_for_url(redirect_pattern)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------

    def expect_error(self, message: str | None = None) -> None:
        """Assert that an error banner is visible, optionally checking its text."""
        self.expect_visible(self.error_banner)
        if message:
            self.expect_text(self.error_banner, message)

    def expect_no_error(self) -> None:
        self.expect_hidden(self.error_banner)
