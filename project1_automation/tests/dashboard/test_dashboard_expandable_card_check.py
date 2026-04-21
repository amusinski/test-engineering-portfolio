
def test_dashboard_expandable_cards_default_and_toggle(page):
    """
    Validates that expandable cards on a dashboard:
    1. Are expanded by default on initial page load.
    2. Collapse when the card header is clicked.
    """

    _log("Navigating to dashboard view.")
    authenticated_navigation(page, "/dashboard")

    # Locate all expandable cards that have a visible title
    cards = page.locator("div.card:has(h2.card-title)")
    cards.first.wait_for(state="visible", timeout=30_000)

    collapsed_on_load = []
    not_collapsed_on_click = []

    def _accordion_panel(card):
        """
        Returns the accordion/collapse panel associated with a card.
        Scoped to avoid false positives like card-body wrappers.
        """
        return card.locator(".accordion-collapse, .collapse").first

    # Pass 1: Validate cards are expanded by default
    for i in range(cards.count()):
        card = cards.nth(i)
        title = card.locator("h2.card-title").first
        card_name = title.inner_text().strip()

        if not card_name:
            continue

        panel = _accordion_panel(card)

        expect(
            panel,
            f"Card '{card_name}' should contain a collapsible panel."
        ).to_have_count(1)

        try:
            expect(
                panel,
                f"Card '{card_name}' should be expanded on initial load."
            ).to_be_visible(timeout=10_000)
        except AssertionError:
            collapsed_on_load.append(card_name)

    if collapsed_on_load:
        raise AssertionError(
            "Cards unexpectedly collapsed on page load: "
            f"{collapsed_on_load}"
        )

    # Pass 2: Validate cards collapse when clicked
    for i in range(cards.count()):
        card = cards.nth(i)
        title = card.locator("h2.card-title").first
        card_name = title.inner_text().strip()

        if not card_name:
            continue

        panel = _accordion_panel(card)

        title.scroll_into_view_if_needed()
        title.click()

        try:
            expect(
                panel,
                f"Card '{card_name}' should collapse after click."
            ).to_be_hidden(timeout=10_000)
        except AssertionError:
            not_collapsed_on_click.append(card_name)

    if not_collapsed_on_click:
        raise AssertionError(
            "Cards did not collapse when clicked: "
            f"{not_collapsed_on_click}"
        )
