"""Utils package — shared helpers and clients."""

from utils.api_client import ApiClient
from utils.helpers import (
    dismiss_cookie_banner,
    get_local_storage,
    measure_time,
    normalize_whitespace,
    retry,
    set_local_storage,
    unique_email,
    unique_username,
    wait_for_network_idle,
)

__all__ = [
    "ApiClient",
    "dismiss_cookie_banner",
    "get_local_storage",
    "measure_time",
    "normalize_whitespace",
    "retry",
    "set_local_storage",
    "unique_email",
    "unique_username",
    "wait_for_network_idle",
]
