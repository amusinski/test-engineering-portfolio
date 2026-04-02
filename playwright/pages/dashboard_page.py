"""
dashboard_page.py — Page Object for the authenticated dashboard.
"""

from __future__ import annotations

from playwright.sync_api import Page

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Encapsulates interactions with the main dashboard after login."""

    PATH = "/dashboard"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.nav = page.get_by_role("navigation")
        self.heading = page.get_by_role("heading", level=1)
        self.user_menu = page.get_by_role("button", name="Account menu")
        self.logout_option = page.get_by_role("menuitem", name="Log out")
        self.notification_badge = page.locator("[data-testid='notification-badge']")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def open(self) -> "DashboardPage":
        self.navigate(self.PATH)
        return self

    def logout(self) -> None:
        """Click the account menu and select Log out."""
        self.click(self.user_menu)
        self.click(self.logout_option)

    # ------------------------------------------------------------------
    # Assertions
    # ------------------------------------------------------------------

    def expect_loaded(self) -> None:
        """Assert that the dashboard has fully loaded."""
        self.expect_visible(self.heading)
        self.expect_visible(self.nav)

    def expect_notification_count(self, count: int) -> None:
        self.expect_text(self.notification_badge, str(count))
