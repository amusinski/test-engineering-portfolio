from playwright.sync_api import expect
from utils.auth import login
from utils.logging import get_logger

log = get_logger("[Dashboard] [Entity Consistency Check]")


def test_dashboard_entities_match_results_filter(page):
    """
    Validate that entities displayed as dashboard cards are consistent with
    selectable entities available in the results/list view.

    This test ensures:
      - All entities visible on the dashboard appear in the results filter
      - Lazy‑loaded dashboard cards are fully collected before comparison
    """

    log("Navigating to dashboard.")
    login(page, path="/dashboard")

    # Capture entity card titles from the dashboard.
    card_title_locator = page.locator("h2.card-title")
    card_title_locator.first.wait_for(state="visible", timeout=10_000)

    dashboard_entity_names: set[str] = set()

    # Because cards may lazy‑load as the user scrolls,
    # collect names until the set stabilizes across iterations.
    stable_rounds = 0
    stable_rounds_required = 2
    max_scroll_rounds = 10

    for _ in range(max_scroll_rounds):
        visible_names = [
            name.strip()
            for name in card_title_locator.all_inner_texts()
            if name and name.strip()
        ]

        size_before = len(dashboard_entity_names)
        dashboard_entity_names.update(visible_names)
        size_after = len(dashboard_entity_names)

        if size_before == size_after:
            stable_rounds += 1
        else:
            stable_rounds = 0

        if stable_rounds >= stable_rounds_required:
            break

        # Scroll to trigger lazy loading of additional cards.
        page.mouse.wheel(0, 2000)
        page.wait_for_timeout(1_000)

    log(f"Collected {len(dashboard_entity_names)} dashboard entities.")

    # Navigate to the results/list view to compare available filter options.
    page.goto("/records", wait_until="domcontentloaded")

    entity_dropdown = page.get_by_role("combobox", name="Entity")
    expect(entity_dropdown).to_be_visible(timeout=10_000)

    dropdown_options = entity_dropdown.locator("option").all_text_contents()

    # Exclude the global 'All' option, which is not an entity.
    results_entity_names = {
        option.strip()
        for option in dropdown_options
        if option and option.strip() and option.strip() != "All"
    }

    log(f"Collected {len(results_entity_names)} result‑filter entities.")

    # The dashboard and results page should represent the same set of entities.
    assert dashboard_entity_names == results_entity_names, (
        "Entity names shown on the dashboard do not match the entities "
        "available in the results filter.\n"
        f"Dashboard only: {dashboard_entity_names - results_entity_names}\n"
        f"Results only: {results_entity_names - dashboard_entity_names}"
    )

    log("PASS: Dashboard entities match results filter entities.")
