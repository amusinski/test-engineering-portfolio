from __future__ import annotations
from datetime import datetime
from urllib.parse import parse_qs, urlparse
from playwright.sync_api import expect
from utils.auth import login
from utils.logging import get_logger

log = get_logger("[Dashboard Summary: Latest Record Date]")


def test_dashboard_latest_record_date_drives_filtered_results(page) -> None:
    """
    Portfolio-safe example: Validate that a dashboard "latest record date" widget:

      - is visible under a summary section
      - has correct tooltip metadata
      - links to a results view with an enabled date-range filter
      - propagates invoice start/end dates through the URL query string
      - yields results whose first row matches the selected date after sorting

    Note: UI labels/selectors are anonymized to avoid disclosing proprietary details.
    """

    # Authenticate once and navigate directly to the dashboard.
    log("Navigating to dashboard.")
    login(page, path="/dashboard/")

    # Select the first visible dashboard card. Avoid assumptions about order or identity.
    card = page.locator("div.card:has(h2.card-title)").first
    expect(card).to_be_visible(timeout=30_000)

    card_title = card.locator("h2.card-title").first.inner_text().strip()
    assert card_title, "Expected the dashboard card to have a visible title."
    log(f"Selected dashboard card: {card_title}")

    # Verify the summary section exists for layout consistency.
    summary_header = card.locator("h3.card-title.primary-text", has_text="Summary").first
    expect(summary_header).to_be_visible(timeout=30_000)

    # Locate the "Latest Record Date" widget label (anonymized name).
    latest_date_label = card.locator("span.metric-label", has_text="Latest Record Date").first
    expect(latest_date_label).to_be_visible(timeout=30_000)
    log("Found widget label: Latest Record Date")

    # Locate tooltip host in the same row as the label and validate its metadata.
    row = latest_date_label.locator("xpath=ancestor::div[contains(@class,'d-flex')][1]")
    expect(row).to_be_visible(timeout=30_000)

    tooltip_icon = row.locator("span[data-bs-toggle='tooltip'] i.bi-info-circle").first
    expect(tooltip_icon).to_be_visible(timeout=30_000)

    tooltip_host = tooltip_icon.locator("xpath=ancestor::span[1]").first
    tooltip_text = (tooltip_host.get_attribute("data-bs-title") or "").strip()
    assert tooltip_text == "Date of the most recent record received.", (
        "Unexpected tooltip text for Latest Record Date widget."
    )

    # Locate the widget link and capture href BEFORE navigation.
    widget = card.locator(
        "div:has(span.metric-label:has-text('Latest Record Date'))"
        ":has(a[href*='/records/'][href*='enable_date_range=on'])"
    ).first
    expect(widget).to_be_visible(timeout=30_000)

    link = widget.locator("a[href*='/records/'][href*='enable_date_range=on']").first
    expect(link).to_be_visible(timeout=30_000)

    displayed_date = link.inner_text().strip()
    assert displayed_date, "Latest Record Date link should display a non-empty date string."
    log(f"Widget displays date text: {displayed_date!r}")

    href = (link.get_attribute("href") or "").strip()
    assert href, "Latest Record Date link should have a non-empty href."

    # Derive expected query params from the href (environment-safe: no absolute host needed).
    href_qs = parse_qs(urlparse(href).query)
    expected_start = (href_qs.get("invoice_start_date") or [""])[0]
    expected_end = (href_qs.get("invoice_end_date") or [""])[0]
    assert expected_start, "Expected invoice_start_date to exist in link href query string."
    assert expected_end, "Expected invoice_end_date to exist in link href query string."

    log(f"Expecting date range start/end: {expected_start} / {expected_end}")

    # Click and verify navigation reached the expected route (do not assert full absolute URL).
    link.click()
    page.wait_for_url("**/records/**", timeout=30_000)

    # Validate URL query reflects the same expected values.
    current_qs = parse_qs(urlparse(page.url).query)
    actual_start = (current_qs.get("invoice_start_date") or [""])[0]
    actual_end = (current_qs.get("invoice_end_date") or [""])[0]

    assert actual_start == expected_start, (
        f"invoice_start_date should be {expected_start!r}, but was {actual_start!r}"
    )
    assert actual_end == expected_end, (
        f"invoice_end_date should be {expected_end!r}, but was {actual_end!r}"
    )

    # Validate UI filter state (selectors anonymized).
    status_dropdown = page.locator("#id_status").first
    expect(status_dropdown).to_be_visible(timeout=30_000)

    selected_status = status_dropdown.locator("option:checked").first.inner_text().strip()
    assert selected_status == "All", (
        f"Status filter should be 'All', but was {selected_status!r}"
    )

    enable_date_range_checkbox = page.locator("#enable-date-range-invoice").first
    expect(enable_date_range_checkbox).to_be_visible(timeout=30_000)
    assert enable_date_range_checkbox.is_checked(), (
        "Expected 'Select specific date range' to be checked."
    )

    invoice_start_input = page.locator("#invoice_start_date").first
    expect(invoice_start_input).to_be_visible(timeout=30_000)
    invoice_start_value = invoice_start_input.input_value().strip()
    assert invoice_start_value == expected_start, (
        f"Invoice Start Date should be {expected_start!r}, but was {invoice_start_value!r}"
    )

    invoice_end_input = page.locator("#invoice_end_date").first
    expect(invoice_end_input).to_be_visible(timeout=30_000)
    invoice_end_value = invoice_end_input.input_value().strip()
    assert invoice_end_value == expected_end, (
        f"Invoice End Date should be {expected_end!r}, but was {invoice_end_value!r}"
    )

    # Sort the results by invoice date so the first row is deterministic.
    sort_link = page.locator("a:has-text('Invoice date')").first
    expect(sort_link).to_be_visible(timeout=30_000)
    sort_link.click()

    # Validate the invoice date shown in the first row matches the expected start date.
    first_invoice_cell = page.locator("td.invoice_date").first
    expect(first_invoice_cell).to_be_visible(timeout=30_000)

    first_invoice_text = first_invoice_cell.inner_text().strip()
    assert first_invoice_text, "Expected the first row to have a visible invoice date."

    # Example UI text: "Nov. 26, 2025" (dot after month). Normalize before parsing.
    normalized = first_invoice_text.replace(".", "")
    parsed_date = datetime.strptime(normalized, "%b %d, %Y").date().isoformat()

    assert parsed_date == expected_start, (
        "First row invoice date should match the selected date range start, "
        f"but was {parsed_date!r} and expected {expected_start!r}"
    )

    log("PASS: Latest Record Date widget correctly drives filter state and results.")
