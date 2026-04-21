UI_TIMEOUT = 30_000

def test_dismiss_record(page: Page) -> None:
    """
    Validates dismissing a record:
    - requires reason + note
    - updates status
    - records audit history
    - enables undo action
    """

    single_use_logins(page)
    verify_default_filters(page)

    set_status_incomplete_requirements(page)
    click_search_button(page)

    record_list_id = str(open_first_record_from_id_column(page))

    click_dismiss_button(page)

    modal = page.locator("[role='dialog']:visible").first
    expect(modal).to_be_visible(timeout=UI_TIMEOUT)

    reason = modal.locator("select[name='reason']")
    reason.select_option("OTHER")

    note = modal.locator("textarea[name='note']")
    note.fill("Automation validation")

    click_confirm_dismiss_button(page)

    success_modal = page.locator("[role='dialog']:visible").first
    expect(success_modal).to_be_visible(timeout=UI_TIMEOUT)

    expect(
        success_modal.locator("p", has_text="successfully dismissed")
    ).to_be_visible(timeout=UI_TIMEOUT)

    success_modal.locator("button", has_text="Close").click()

    header = page.locator("h4", has_text=re.compile(r"\[\d+]"))
    record_id = re.search(r"\[(\d+)]", header.inner_text()).group(1)

    assert record_id == record_list_id

    undo_button = page.locator("#undo-dismiss-button")
    expect(undo_button).to_be_enabled()

    history_new = page.locator("td[id^='new-history-']", has_text="DISMISSED")
    expect(history_new).to_be_visible(timeout=UI_TIMEOUT)
