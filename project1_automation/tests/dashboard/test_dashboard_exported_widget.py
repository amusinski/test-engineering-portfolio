
def test_dashboard_exported_items_last_30_days(page):
    """
    Validate the 'Exported Items (Last 30 Days)' metric on a dashboard card.

    This test verifies:
      - Metric visibility within the summary section
      - Tooltip text accurately describes the metric
      - Metric counter links to a filtered results view
      - Filtered result count matches the dashboard metric
    """

    # Authenticate once and navigate directly to the dashboard.
    # Authentication is intentionally abstracted to keep this test
    # focused on contract-level UI validation.
    log("Navigating to dashboard.")
    login(page, path="/dashboard/")

    # Select the first available dashboard card.
    # The test avoids relying on card order or specific entity names.
    first_card = page.locator("div.card:has(h2.card-title)").first
    expect(first_card).to_be_visible(timeout=30_000)

    card_title = first_card.locator("h2.card-title").first.inner_text().strip()
    assert card_title, "Expected the dashboard card to have a visible title."

    log(f"Selected dashboard card: {card_title}")

    # Verify the summary section exists for layout consistency.
    summary_header = first_card.locator(
        "h3.card-title.primary-text",
        has_text="Summary",
    ).first
    expect(summary_header).to_be_visible(timeout=30_000)

    # Locate the Exported Items metric label.
    exported_metric_label = first_card.locator(
        "span.metric-label",
        has_text="Exported Items (Last 30 Days)",
    ).first
    expect(exported_metric_label).to_be_visible(timeout=30_000)

    log("Found metric label: Exported Items (Last 30 Days)")

    # Locate the tooltip icon associated with the metric.
    # Using ancestor scoping ensures the tooltip belongs to this metric row.
    metric_row = exported_metric_label.locator(
        "xpath=ancestor::div[contains(@class,'d-flex')][1]"
    )
    expect(metric_row).to_be_visible(timeout=30_000)

    tooltip_icon = metric_row.locator(
        'span[data-bs-toggle="tooltip"] i.bi-info-circle'
    ).first
    expect(tooltip_icon).to_be_visible(timeout=30_000)

    # Validate tooltip text via the host element attribute.
    # Reading from the attribute avoids flakiness from rendered tooltip DOMs.
    tooltip_host = tooltip_icon.locator("xpath=ancestor::span[1]").first
    tooltip_text = (tooltip_host.get_attribute("data-bs-title") or "").strip()

    assert tooltip_text == "Records that have been previously batched.", (
        "Unexpected tooltip text for exported items metric."
    )

    # Locate the metric counter link scoped to both label and filter intent.
    metric_widget = first_card.locator(
        "div:has(span.metric-label:has-text('Exported Items (Last 30 Days)'))"
        ":has(a[href*='exported_date=30'])"
    ).first
    expect(metric_widget).to_be_visible(timeout=30_000)

    counter_link = metric_widget.locator("a[href*='exported_date=30']").first
    expect(counter_link).to_be_visible(timeout=30_000)

    counter_value = counter_link.inner_text().strip()
    assert counter_value.isdigit(), (
        "Exported Items counter should be a non-negative integer, "
        f"but was {counter_value!r}"
    )

    log(f"Metric counter value: {counter_value}")

    # Navigate to the filtered results view by clicking the metric.
    counter_link.click()

    # Validate filter state matches the metric context.
    status_filter = page.locator("#id_status").first
    expect(status_filter).to_be_visible(timeout=30_000)

    selected_status = (
        status_filter.locator("option:checked").first.inner_text().strip()
    )
    assert selected_status == "Exported", (
        f"Expected status filter 'Exported', but was {selected_status!r}"
    )

    date_filter = page.locator("#id_exported_date").first
    expect(date_filter).to_be_visible(timeout=30_000)

    selected_date_range = (
        date_filter.locator("option:checked").first.inner_text().strip()
    )
    assert selected_date_range == "Last 30 Days", (
        f"Expected date range 'Last 30 Days', but was {selected_date_range!r}"
    )

    # Validate that the results page reflects the dashboard metric count.
    total_count_el = page.locator("p:has-text('Total Record Count')").first
    expect(total_count_el).to_be_visible(timeout=30_000)

    total_count_text = total_count_el.inner_text().strip()
    total_count = total_count_text.replace("Total Record Count", "").strip()

    assert total_count.isdigit(), (
        f"Total Record Count should be numeric, but was {total_count_text!r}"
    )

    assert int(total_count) == int(counter_value), (
