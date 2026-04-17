from playwright.sync_api import expect
from utils.auth import login
from utils.logging import get_logger
import re

log = get_logger("[Dashboard Category Widget Validation]")


def test_dashboard_category_widget_features(page):
    """
    Validate category-level summary widgets on a dashboard card.

    This test verifies:
    - Tooltip copy and value formatting for category metrics
    - Numeric counters are reflected correctly in the records view
    - Dashboard aggregates remain consistent with filtered results
    """

    log("Navigating to dashboard.")
    login(page, path="/dashboard")

    # Select the first available dashboard card
    card = page.locator("div.card:has(h2.card-title)").first
    expect(card).to_be_visible(timeout=30_000)

    entity_name = card.locator("h2.card-title").first.inner_text().strip()
    assert entity_name, "Dashboard card should have a visible entity name."

    log(f"Selected entity: {entity_name}")

    # Select the first category widget within the card
    category_header = card.locator("h5").first
    expect(category_header).to_be_visible(timeout=30_000)

    category_name = category_header.inner_text().strip()
    assert category_name, "Expected at least one category widget."

    log(f"Selected category: {category_name}")

    def assert_row_tooltip_and_value(
        label: str,
        expected_tooltip: str | None,
        *,
        numeric_value: bool,
        alternate_tooltips: tuple[str, ...] = (),
    ) -> str:
        row = card.locator(f'li:has-text("{label}")').first
        expect(row).to_be_visible(timeout=30_000)

        tooltip_host = row.locator("span[data-bs-toggle='tooltip']").first
        tooltip_text = (tooltip_host.get_attribute("data-bs-title") or "").strip()

        accepted = tuple(t.strip() for t in alternate_tooltips if t.strip())
        if expected_tooltip:
            accepted = (expected_tooltip.strip(),) + accepted

        assert tooltip_text in accepted, (
            f"Unexpected tooltip for {label!r}: {tooltip_text!r}"
        )

        if numeric_value:
            value = row.locator("p.ms-auto").first.inner_text().strip()
            assert value.isdigit(), f"{label} value should be numeric."
            return value

        value = row.locator("span.fw-bold").first.inner_text().strip()
        assert re.fullmatch(r"\d{2}/\d{2}/\d{4}", value), (
            f"{label} should be formatted as MM/DD/YYYY."
        )
        return value

    ready_count = assert_row_tooltip_and_value(
        "Ready",
        "Records that are complete and ready for processing.",
        numeric_value=True,
    )

    incomplete_count = assert_row_tooltip_and_value(
        "Incomplete",
        "Records missing required data.",
        numeric_value=True,
    )

    expired_count = assert_row_tooltip_and_value(
        "Expired",
        None,
        numeric_value=True,
        alternate_tooltips=(
            "Record does not meet eligibility requirements.",
            "Record no longer qualifies based on policy rules.",
        ),
    )

    last_processed_date = assert_row_tooltip_and_value(
        "Last Processed Date",
        "Records that have been processed previously.",
        numeric_value=False,
    )

    # Navigate to records view and validate counters
    page.goto("/records", wait_until="domcontentloaded")

    entity_filter = page.locator("#entity_filter")
    expect(entity_filter).to_be_visible()
    entity_filter.select_option(label=entity_name)

    category_filter = page.locator("#category_filter")
    expect(category_filter).to_be_visible()
    category_filter.select_option(label=category_name)

    status_filter = page.locator("#status_filter")
    expect(status_filter).to_be_visible()

    search_button = page.locator('button:has-text("Search")')

    def assert_record_count(expected: int, status_label: str):
        status_filter.select_option(label=status_label)
        search_button.click()

        count_text = page.locator(
            'p:has-text("Total Record Count")'
        ).inner_text()
        match = re.search(r"(\d+)$", count_text)
        assert match, "Could not read Total Record Count."

        actual = int(match.group(1))
        assert actual == expected, (
            f"{status_label} count mismatch: expected {expected}, got {actual}"
        )

    assert_record_count(int(ready_count), "Ready")
    assert_record_count(int(incomplete_count), "Incomplete")
    assert_record_count(int(expired_count), "Expired")

    log("PASS: Category widget values match filtered record counts.")
