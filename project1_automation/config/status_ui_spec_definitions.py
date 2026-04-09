from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class StatusUiSpec:
    """
    Define the UI expectations for a given status value.
    """
    required_icon_selectors: tuple[str, ...]
    must_contain: tuple[str, ...]

STATUS_UI_SPECS: dict[str, StatusUiSpec] = {
    "exported": StatusUiSpec(
        required_icon_selectors=(
            "i",
        ),
        must_contain=(
            "Exported",
        ),
    ),
    "expired": StatusUiSpec(
        required_icon_selectors=(
            "i",
        ),
        must_contain=(
            "Expired",
        ),
    ),
    "incomplete_requirements": StatusUiSpec(
        required_icon_selectors=(
            "i",
        ),
        must_contain=(
            "Incomplete Requirements",
        ),
    ),
    "dismissed": StatusUiSpec(
        required_icon_selectors=(
            "i",
        ),
        must_contain=(
            "Dismissed",
        ),
    ),
}
