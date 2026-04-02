"""
test_login.py — Example test suite for the login flow.

Demonstrates:
  - Page Object Model usage
  - Parametrised test cases
  - Negative / security-focused scenarios
  - pytest markers for CI pipeline targeting
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(page: Page) -> None:
    """A user with valid credentials should land on the dashboard."""
    login = LoginPage(page).open()
    login.login_and_wait("testuser@example.com", "Test1234!")
    assert "/dashboard" in page.url


# ---------------------------------------------------------------------------
# Authentication error scenarios
# ---------------------------------------------------------------------------


@pytest.mark.regression
@pytest.mark.parametrize(
    ("email", "password", "expected_error"),
    [
        ("testuser@example.com", "WrongPassword!", "Invalid email or password"),
        ("notregistered@example.com", "Test1234!", "Invalid email or password"),
        ("bad-email-format", "Test1234!", "Please enter a valid email address"),
        ("", "Test1234!", "Email is required"),
        ("testuser@example.com", "", "Password is required"),
    ],
    ids=[
        "wrong_password",
        "unknown_email",
        "invalid_email_format",
        "empty_email",
        "empty_password",
    ],
)
def test_invalid_login_shows_error(
    page: Page,
    email: str,
    password: str,
    expected_error: str,
) -> None:
    """Invalid credential combinations should show appropriate errors."""
    login = LoginPage(page).open()
    login.login(email, password)
    login.expect_error(expected_error)


# ---------------------------------------------------------------------------
# Security: no user enumeration
# ---------------------------------------------------------------------------


@pytest.mark.regression
def test_error_message_does_not_enumerate_users(page: Page) -> None:
    """
    Both 'wrong password' and 'unknown user' should return the same generic
    error message to prevent user enumeration attacks.
    """
    login = LoginPage(page).open()

    login.login("testuser@example.com", "WrongPassword!")
    wrong_password_error = login.error_banner.inner_text()

    login.open()
    login.login("nobody@example.com", "Test1234!")
    unknown_user_error = login.error_banner.inner_text()

    assert wrong_password_error == unknown_user_error, (
        "Different error messages for wrong-password vs unknown-user "
        "leak user existence — fix before shipping."
    )


# ---------------------------------------------------------------------------
# Session management
# ---------------------------------------------------------------------------


@pytest.mark.regression
def test_authenticated_session_persists_on_reload(page: Page) -> None:
    """After login, refreshing the page should keep the user logged in."""
    login = LoginPage(page).open()
    login.login_and_wait("testuser@example.com", "Test1234!")

    page.reload()
    assert "/dashboard" in page.url, "User was logged out after page reload"
