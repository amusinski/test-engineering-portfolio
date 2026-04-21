
def test_dashboard_unassigned_items_metric(page):
    """
    Validate the 'Unassigned Items' metric on a dashboard card.

    This test verifies:
      - Metric visibility within the dashboard summary section
      - Tooltip text accurately describes the metric
      - Metric counter links to a filtered results view
      - Filtered results reflect the dashboard metric count
    """

    # Authenticate once and navigate directly to the dashboard.
    log("Navigating to dashboard.")
    login(page, path="/dashboard/")

    # Select the first available dashboard card.
    # The test avoids assumptions about card ordering or specific entities.
    first_card = page.locator("div.card:has(h2.card-title)").first
    expect(first_card).to_be_visible(timeout=30_000)

    card_title = first_card.locator("h2.card-title").first.inner_text().strip()
    assert card_title, "Expected the dashboard card to have a visible title."

    log(f"Selected dashboard card: {card_title}")

    # Validate the presence of the summary section for layout consistency.
    summary_header = first_card.locator(
        "h3.card-title.primary-text",
        has_text="Summary",
    ).first
    expect(summary_header).to_be_visible(timeout=30_000)

    # Locate the Unassigned Items metric label.
    unassigned_label = first_card.locator(
        "span.metric-label",
        has_text="Unassigned Items",
    ).first
    expect(unassigned_label).to_be_visible(timeout=30_000)

    log("Found metric label: Unassigned Items")

    # Scope to the metric row to ensure tooltip and counter associations
    # are validated in the correct context.
    metric_row = unassigned_label.locator(
        "xpath=ancestor::div[contains(@class,'d-flex')][1]"
    )
    expect(metric_row).to_be_visible(timeout=30_000)

    # Validate tooltip metadata via the host element attribute.
    # Reading tooltip text from attributes avoids reliance on rendered DOM.
    tooltip_host = metric_row.locator(
        "span[data-bs-toggle='tooltip']"
    ).first
    expect(tooltip_host).to_be_visible(timeout=30_000)

    tooltip_text = (tooltip_host.get_attribute("data-bs-title") or "").strip()
    assert tooltip_text == "Records that did not match a program.", (
        "Unexpected tooltip text for Unassigned Items metric."
    )

    # Validate that the info icon is present for user discoverability.
    tooltip_icon = tooltip_host.locator("i.bi-info-circle").first
    expect(tooltip_icon).to_be_visible(timeout=30_000)

    # Locate the metric counter hyperlink associated with the Unassigned filter.
    metric_widget = first_card.locator(
        "div:has(span.metric-label:has-text('Unassigned Items'))"
        ":has(a[href*='status=UNASSIGNED'])"
    ).first
    expect(metric_widget).to_be_visible(timeout=30_000)

    counter_link = metric_widget.locator(
        "a[href*='status=UNASSIGNED']"
    ).first
    expect(counter_link).to_be_visible(timeout=30_000)

    counter_value = counter_link.inner_text().strip()
    assert counter_value.isdigit(), (
        "Unassigned Items counter should be a non-negative integer, "
        f"but was {counter_value!r}"
    )

    log(f"Metric counter value: {counter_value}")

    # Navigate to the filtered results view via the metric counter.
    counter_link.click()

    # Validate filter state matches the metric context.
    status_filter = page.locator("#id_status").first
    expect(status_filter).to_be_visible(timeout=30_000)

    selected_status = (
        status_filter.locator("option:checked").first.inner_text().strip()
    )
    assert selected_status == "Unassigned", (
        f"Expected status filter 'Unassigned', but was {selected_status!r}"
    )

    selected_status_value = (
        status_filter.locator("option:checked").first.get_attribute("value") or ""
    ).strip()
    assert selected_status_value == "UNASSIGNED", (
        f"Expected status value 'UNASSIGNED', but was {selected_status_value!r}"
    )

    # Validate that unrelated filters are not implicitly constrained.
    invoice_date_filter = page.locator("#id_invoice_date").first
    expect(invoice_date_filter).to_be_visible(timeout=30_000)

    selected_invoice_date = (
        invoice_date_filter.locator("option:checked").first.inner_text().strip()
    )
    assert selected_invoice_date == "All", (
        f"Expected invoice date filter 'All', but was {selected_invoice_date!r}"
    )

    # Cross‑validate dashboard metric count against filtered results total.
    total_count_el = page.locator("p:has-text('Total Record Count')").first
    expect(total_count_el).to_be_visible(timeout=30_000)

    total_count_text = total_count_el.inner_text().strip()
    total_count = total_count_text.replace("Total Record Count", "").strip()

    assert total_count.isdigit(), (
        f"Total Record Count should be numeric, but was {total_count_text!r}"
    )

    assert int(total_count) == int(counter_value), (
        "Total Record Count should match Unassigned Items dashboard metric, "
        f"but was {total_count} vs {counter_value}"
    )

    log(
        f"PASS: Unassigned Items metric validated — dashboard value "
        f"({counter_value}) matches filtered results ({total_count})."
    )
