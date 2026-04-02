"""
test_accessibility.py — Accessibility smoke tests.

Uses axe-core via the assert_no_violations fixture to verify that key pages
meet WCAG 2.1 AA criteria automatically on every build.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import Page


@pytest.mark.smoke
@pytest.mark.parametrize(
    "path",
    ["/login", "/register", "/forgot-password"],
    ids=["login", "register", "forgot_password"],
)
def test_unauthenticated_pages_have_no_axe_violations(
    page: Page,
    assert_no_violations,
    path: str,
) -> None:
    """Public pages must have zero axe-core critical/serious violations."""
    page.goto(path)
    assert_no_violations()


@pytest.mark.regression
def test_dashboard_has_no_axe_violations(
    authenticated_page: Page,
    assert_no_violations,
) -> None:
    authenticated_page.goto("/dashboard")
    assert_no_violations()
