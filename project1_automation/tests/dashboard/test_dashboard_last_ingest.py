import re

from test_helpers import make_log, single_use_logins

_log = make_log("[UI][Dashboard][Last Update Widget]")


def test_last_update_widget(page):
    """
    Validates the presence and date format of the 'Last Update' widget
    within the Data Summary section of the Dashboard.
    """

    # Single-use login prevents state leakage between UI tests.
    _log("Navigating to Dashboard.")
    single_use_logins(page, "/dashboard/")

    # Locate the first visible summary card on the dashboard.
    summary_card = page.locator("div.card:has(h2.card-title)").first
    summary_card.wait_for(state="visible", timeout=30_000)

    # Confirm the expected section exists within the card.
    data_summary_title = summary_card.locator(
        "h3.card-title",
        has_text="Data Summary",
    ).first
    data_summary_title.wait_for(state="visible", timeout=30_000)

    assert data_summary_title.inner_text().strip() == "Data Summary"
    _log("Confirmed section: Data Summary")

    # Locate the 'Last Update' label within this section.
    last_update_label = summary_card.locator(
        "span.card-link",
        has_text="Last Update",
    ).first
    last_update_label.wait_for(state="visible", timeout=30_000)

    assert last_update_label.inner_text().strip() == "Last Update"
    _log("Found widget label: Last Update")

    # Intentional pause for interactive debugging; safe to remove for CI-only runs.
    page.wait_for_timeout(1200)

    # Walk up the DOM to the smallest container that includes the update date.
    last_update_widget = last_update_label.locator(
        "xpath=ancestor::*[self::div or self::li]"
        "[.//p[contains(@class,'card-text') and contains(., 'Updated on')]][1]"
    ).first
    last_update_widget.wait_for(state="visible", timeout=30_000)

    # Extract the rendered update date.
    updated_on_span = last_update_widget.locator(
        "p:has-text('Updated on') span"
    ).first
    updated_on_span.wait_for(state="visible", timeout=30_000)

    updated_on_text = updated_on_span.inner_text().strip()

    # Validate UI contract: mm/dd/yyyy
    assert re.fullmatch(r"\d{2}/\d{2}/\d{4}", updated_on_text), (
        "Expected 'Updated on' date format mm/dd/yyyy, "
        f"but found {updated_on_text!r}"
    )

    _log(f"Validated update date format: {updated_on_text}")
