from __future__ import annotations
from playwright.sync_api import expect
from utils.auth import login
from utils.logging import get_logger

log = get_logger("[Dashboard Default View]")


def test_dashboard_default_view(page) -> None:
    """
    Validate the default dashboard view renders correctly.

    The test intentionally focuses on structural and contract-level validation:
      - At least one dashboard card is rendered
      - Each card has a visible title and summary section
      - Required summary metrics appear exactly once per card
      - Optional section widgets are captured for observability rather than strict assertion
    """
    # Navigate directly to the dashboard as an authenticated user.
    # Authentication is abstracted to keep the test focused on UI validation.
    log("Navigating to dashboard.")
    login(page, path="/dashboard/")

    # Locate all visible dashboard cards by structure rather than index
    # to avoid ordering assumptions.
    cards = page.locator("div.card:has(h2.card-title)")
    expect(cards.first).to_be_visible(timeout=30_000)

    card_count = cards.count()
    assert card_count >= 1, "Expected at least one dashboard card to be rendered."

    log(f"Found {card_count} dashboard card(s). Validating default view.")

    required_summary_labels = [
        "Metric A (Last 30 Days)",
        "Last Update",
        "Unassigned Items",
        "Recently Dismissed",
        "Latest Record Date",
    ]

    # Collected for diagnostic visibility rather than enforcement;
    # section/widget presence may legitimately vary by data context.
    widgets_by_card: dict[str, list[str]] = {}

    for i in range(card_count):
        card = cards.nth(i)

        # Validate the card title exists and is readable.
        # An empty title usually indicates a rendering or data-binding issue.
        title = card.locator("h2.card-title").first
        expect(title).to_be_visible(timeout=30_000)

        card_name = title.inner_text().strip()
        assert card_name, f"Dashboard card at index {i} has an empty title."

        log(f"[{i + 1}/{card_count}] Card title: {card_name}")

        # Validate the presence of the summary section header.
        # This ensures consistent layout and user expectations across cards.
        summary_header = card.locator(
            "h3.card-title.primary-text",
            has_text="Summary",
        ).first

        expect(
            summary_header,
            f"Card '{card_name}' should display a summary section header.",
        ).to_be_visible(timeout=30_000)

        # Each required metric should appear exactly once.
        # This guards against duplicate rendering and missing data states.
        for label in required_summary_labels:
            label_locator = card.locator(
                "span.metric-label",
                has_text=label,
            )

            expect(
                label_locator,
                f"Card '{card_name}' should contain exactly one summary label '{label}'.",
            ).to_have_count(1, timeout=30_000)

            expect(label_locator.first).to_be_visible(timeout=30_000)

        # Section widgets are optional and data-driven.
        # The test validates visibility and content without asserting a fixed count.
        section_widgets = card.locator("h5.primary-text")
        section_names: list[str] = []

        for j in range(section_widgets.count()):
            widget = section_widgets.nth(j)
            expect(widget).to_be_visible(timeout=30_000)

            widget_name = widget.inner_text().strip()
            assert widget_name, (
                f"Section widget at index {j} on card '{card_name}' has empty text."
            )

            section_names.append(widget_name)

        widgets_by_card[card_name] = section_names

        if section_names:
            log(f"  Section widgets: {section_names}")
        else:
            log("  Section widgets: NONE")

    # Emit a consolidated summary to aid log-based debugging,
    # particularly when analyzing CI failures or historical runs.
    log("----- Section Widget Summary (By Card) -----")
    for card_name, section_names in widgets_by_card.items():
        if section_names:
            log(f"{card_name}: {section_names}")
        else:
            log(f"{card_name}: NONE")

    log(
        "PASS: Dashboard default view validated — cards rendered, "
        "summary metrics verified, and optional section widgets observed."
    )
