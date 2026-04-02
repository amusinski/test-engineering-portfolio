"""Pages package — export all page objects for convenient imports."""

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage

__all__ = ["BasePage", "DashboardPage", "LoginPage"]
