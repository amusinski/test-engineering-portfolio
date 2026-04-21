
def test_dashboard_dismissed_items_last_30_days(page):
    """
    Validate the 'Dismissed Items (Last 30 Days)' metric on a dashboard card.

    This test verifies:
      - The metric is visible within the card summary section
      - The tooltip content explains the metric correctly
      - The metric counter links to a filtered results view
      - The filtered result count matches the dashboard counter
    """

    # Authenticate once and navigate directly to the dashboard to avoid
    # unnecessary cross-test session state.
    log("Navigating to dashboard.")
    login(page, path="/dashboard/")

    # Select the first available dashboard card.
    # The test intentionally avoids relying on ordering guarantees.
    first_card = page.locator("div.card:has(h2.card-title)").first
    expect(first_card).to_be_visible(timeout=30_000)

    card_title = first_card.locator("h2.card-title").first.inner_text().strip()
    assert card_title, "Expected the dashboard card to have a visible title."

    log(f"Selected dashboard card: {card_title}")

    # Locate the summary section within the selected card.
    summary_header = first_card.locator(
        "h3.card-title.primary-text",
        has_text="Summary",
    ).first
    expect(summary_header).to_be_visible(timeout=30_000)

    # Validate presence of the metric label.
    dismissed_metric_label = first_card.locator(
        "span.metric-label",
        has_text="Dismissed Items (Last 30 Days)",
    ).first
    expect(dismissed_metric_label).to_be_visible(timeout=30_000)

    log("Found metric label: Dismissed Items (Last 30 Days)")

    # Locate the tooltip trigger associated with the metric.
    # The ancestor selector ensures we remain scoped to the metric row.
    metric_row = dismissed_metric_label.locator(
        "xpath=ancestor::div[contains(@class,'d-flex')][1]"
    )
    expect(metric_row).to_be_visible(timeout=30_000)

    tooltip_icon = metric_row.locator(
        'span[data-bs-toggle="tooltip"] i.bi-info-circle'
    ).first
    expect(tooltip_icon).to_be_visible(timeout=30_000)

    # Validate tooltip text from its host element rather than rendered DOM,
    # as this is more stable and CI-friendly.
    tooltip_host = tooltip_icon.locator("xpath=ancestor::span[1]").first
    tooltip_text = (tooltip_host.get_attribute("data-bs-title") or "").strip()

    assert tooltip_text == (
        "Records that have been archived because they cannot be completed."
    ), "Unexpected tooltip description for dismissed items metric."

    # Locate the metric counter link.
    # The selector intentionally validates both label context and filter intent.
    metric_widget = first_card.locator(
        "div:has(span.metric-label:has-text('Dismissed Items (Last 30 Days)'))"
        ":has(a[href*='status=DISMISSED'][href*='date_range=30'])"
    ).first
    expect(metric_widget).to_be_visible(timeout=30_000)

    counter_link = metric_widget.locator(
        "a[href*='status=DISMISSED'][href*='date_range=30']"
    ).first
    expect(counter_link).to_be_visible(timeout=30_000)

    counter_value = counter_link.inner_text().strip()
    assert counter_value.isdigit(), (
        "Metric counter should be a non-negative integer, "
        f"but was {counter_value!r}"
    )

    log(f"Metric counter value: {counter_value}")

    # Click through to the filtered results view.
    counter_link.click()

    # Validate filter state is preserved on navigation.
    status_filter = page.locator("#id_status").first
    expect(status_filter).to_be_visible(timeout=30_000)

    selected_status = (
        status_filter.locator("option:checked").first.inner_text().strip()
    )
    assert selected_status == "Dismissed", (
        f"Expected status filter 'Dismissed', but was {selected_status!r}"
    )

    date_filter = page.locator("#id_date_range").first
    expect(date_filter).to_be_visible(timeout=30_000)

    selected_date_range = (
        date_filter.locator("option:checked").first.inner_text().strip()
    )
    assert selected_date_range == "Last 30 Days", (
        f"Expected date range 'Last 30 Days', but was {selected_date_range!r}"
    )

    # Cross‑validate dashboard metric count against filtered results total.
    total_count_el = page.locator("p:has-text('Total Record Count')").first
