from __future__ import annotations
from playwright.sync_api import Page, expect
from config.settings import base_url, url
import os

def login_via_entra_sso(page: Page, *, destination: str = "/dashboard/") -> None:
    """
    Sign in through the organization's Microsoft Entra SSO flow and wait until
    the application finishes loading the requested destination.

    Args:
        page: Playwright page used for the browser session.
        destination: Application path to open after authentication.
    """
    # Open the application entry point.
    page.goto(base_url(), wait_until="domcontentloaded")

    # Start the SSO flow.
    page.get_by_role("button", name="SSO Login").click()

    # Populate the username step.
    username_input = page.locator("#i0116")
    username_input.wait_for(state="visible", timeout=30_000)
    username_input.fill(os.environ["SSO_USERNAME"])

    page.locator("#idSIButton9").click()

    # Populate the password step.
    password_input = page.locator("#i0118")
    password_input.wait_for(state="visible", timeout=30_000)
    password_input.fill(os.environ["SSO_PASSWORD"])

    page.locator("#idSIButton9").click()

    # Handle any "Stay signed in?" prompt if it appears.
    stay_signed_in_button = page.locator("#idSIButton9")
    try:
        stay_signed_in_button.wait_for(state="visible", timeout=5_000)
        stay_signed_in_button.click()
    except Exception:
        pass

    # Wait for the app to finish loading and navigate to the requested page.
    expect(page).to_have_url(url(destination), timeout=60_000)
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")
