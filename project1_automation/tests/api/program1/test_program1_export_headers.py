from __future__ import annotations
from pathlib import Path
import allure

from api_utility import load_export_cases, validate_export_case

# The JSON file is the single source of truth for export expectations.
CASES_FILE = Path(__file__).with_name("program_export_column_headers.json")


@allure.feature("API")
@allure.story("Program export downloads")
def test_program_export_column_headers(authed_request_context) -> None:
    """
    Validate one or more program export downloads against the expectations stored
    in the JSON case file beside this test.
    """
    cases = load_export_cases(CASES_FILE)

    for case in cases:
        allure.dynamic.title(f"{case.name} export headers match expected values")
        validate_export_case(authed_request_context, case)
