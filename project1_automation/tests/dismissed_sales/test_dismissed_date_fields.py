def _assert_date_within_last_days(date_value: str, days: int) -> None:
    """
    Assert that a yyyy-mm-dd date extracted from the given value
    falls within the last `days` days (inclusive), using UTC to
    avoid local timezone discrepancies.
    """
    date_str = date_value.strip()[:10]
    dismissed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

    today = datetime.utcnow().date()
    delta_days = (today - dismissed_date).days

    assert 0 <= delta_days <= days, (
        f"Dismissed date {dismissed_date} is not within the last {days} days "
        f"(today={today}, delta_days={delta_days})."
    )
