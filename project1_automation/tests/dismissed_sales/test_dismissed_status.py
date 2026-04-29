from playwright.sync_api import Locator
import pytest


# -------------------------------------------------------------------
# Shared UI assertion helper
# -------------------------------------------------------------------

def assert_status_cell_matches_spec(cell: Locator, *, status_key: str, specs: dict) -> None:
    """
    Validates that a status table cell conforms to a predefined UI specification.

    - Confirms required icons are present
    - Confirms required text fragments are visible
    """
    spec = specs[status_key]

    # Validate required icons
    for selector in spec["required_icon_selectors"]:
        assert cell.locator(selector).count() >= 1, (
            f"Expected status cell to contain icon {selector!r} "
            f"for status {status_key!r}."
        )

    # Validate required text fragments
    cell_text = cell.inner_text().strip()
    for expected_text in spec["must_contain"]:
        assert expected_text in cell_text, (
            f"Expected status cell to contain {expected_text!r} "
            f"for status {status_key!r}, but found {cell_text!r}."
        )


# -------------------------------------------------------------------
# End-to-end UI test
# -------------------------------------------------------------------

def test_filtered_results_status_field(page):
    """
    Verifies that filtering results by a specific status:
    - Loads results correctly
    - Displays the expected status indicators in the first row
    - Maintains correctness when sorting the Status column
    """

    def log(msg: str) -> None:
        print(f"[UI][Status Test] {msg}")

    def highlight(element, *, color: str = "#0a84ff", wait_ms: int = 300) -> None:
        """Visually highlights an element during test execution (debug aid)."""
        element.scroll_into_view_if_needed()
        element.evaluate(
            f"""
            (node) => {{
                node.style.outline = '3px solid {color}';
                node.style.outlineOffset = '3px';
                node.style.background = 'rgba(10, 132, 255, 0.10)';
                node.style.borderRadius = '4px';
            }}
            """
        )
        page.wait_for_timeout(wait_ms)

    # Navigate to a generic data listing page
    log("Navigating to data listing page.")
    page.goto("/data", wait_until="domcontentloaded")
    page.wait_for_url("**/data**", timeout=30_000)

    # Apply filter: Category
    log("Selecting Category filter.")
    category_select = page.locator("#id_category")
    category_select.wait_for(state="visible", timeout=30_000)
    highlight(category_select)
    category_select.select_option(label="Example Category")

    # Apply filter: Status
    log("Selecting Status filter.")
    status_select = page.locator("#id_status")
    status_select.wait_for(state="visible", timeout=30_000)
    highlight(status_select)
    status_select.select_option(label="Dismissed")

    # Submit search
    log("Submitting search.")
    search_button = page.locator("button[type='submit']", has_text="Search")
    search_button.wait_for(state="visible", timeout=30_000)
    highlight(search_button, color="#34c759")
    search_button.click()

    # Handle empty state deterministically
    empty_state = page.locator('p:has-text("Total Record Count 0")')
    first_status_cell = page.locator("td.status").first

    log("Waiting for results or empty state.")
    try:
        first_status_cell.wait_for(state="visible", timeout=10_000)
        has_results = True
    except Exception:
        has_results = False

    if not has_results:
        if empty_state.is_visible():
            pytest.skip("No results returned for selected filters.")
        else:
            raise AssertionError(
                "Neither results nor empty state were rendered."
            )

    # Verify first-row status cell
    def verify_status_cell(cell: Locator, *, stage: str) -> None:
        log(f"Verifying Status cell ({stage}).")
        highlight(cell, color="#ff9f0a")

        cell_text = cell.inner_text().strip()
        assert cell_text, "Expected Status cell text to be non-empty."

        help_text = cell.locator(".help-text")
        help_text_value = help_text.first.inner_text().strip() if help_text.count() else ""

        assert (
            "Dismissed" in cell_text or "Dismissed" in help_text_value
        ), "Expected 'Dismissed' to appear in Status cell."

        assert cell.locator("i").count() >= 1, (
            "Expected at least one icon indicating status."
        )

    verify_status_cell(first_status_cell, stage="initial")

    # Sort by Status column
    log("Sorting by Status column.")
    status_header = page.get_by_role("link", name="Status")
    status_header.first.click()
    verify_status_cell(page.locator("td.status").first, stage="sorted asc")

    status_header.first.click()
    verify_status_cell(page.locator("td.status").first, stage="sorted desc")

    log("Status field validation passed across filtering and sorting.")
