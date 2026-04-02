"""
api_client.py — Lightweight wrapper around requests for API-level test setup.

Use this for fast, headless precondition setup (creating users, seeding data)
before a Playwright test takes over the UI.
"""

from __future__ import annotations

import os
from typing import Any

import requests

BASE_URL: str = os.environ.get("BASE_URL", "http://localhost:3000")
API_KEY: str = os.environ.get("TEST_API_KEY", "")


class ApiClient:
    """
    Thin HTTP client for test setup and teardown.

    All methods raise ``requests.HTTPError`` on non-2xx responses so that
    test setup failures are loud and obvious.

    Example::

        client = ApiClient()
        user = client.create_user(email="alice@example.com", password="Secret1!")
        # ... run Playwright tests using alice's account ...
        client.delete_user(user["id"])
    """

    def __init__(self, base_url: str = BASE_URL, api_key: str = API_KEY) -> None:
        self._session = requests.Session()
        self._base_url = base_url.rstrip("/")
        if api_key:
            self._session.headers["X-API-Key"] = api_key

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        resp = self._session.get(self._url(path), **kwargs)
        resp.raise_for_status()
        return resp

    def post(self, path: str, json: Any = None, **kwargs: Any) -> requests.Response:
        resp = self._session.post(self._url(path), json=json, **kwargs)
        resp.raise_for_status()
        return resp

    def patch(self, path: str, json: Any = None, **kwargs: Any) -> requests.Response:
        resp = self._session.patch(self._url(path), json=json, **kwargs)
        resp.raise_for_status()
        return resp

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        resp = self._session.delete(self._url(path), **kwargs)
        resp.raise_for_status()
        return resp

    # ------------------------------------------------------------------
    # Domain-level helpers (extend as needed)
    # ------------------------------------------------------------------

    def create_user(self, email: str, password: str, **extra: Any) -> dict[str, Any]:
        """Create a test user and return the response body."""
        return self.post("/api/users", json={"email": email, "password": password, **extra}).json()

    def delete_user(self, user_id: str) -> None:
        """Hard-delete a test user by ID."""
        self.delete(f"/api/users/{user_id}")

    def health_check(self) -> bool:
        """Return True if the application is healthy and reachable."""
        try:
            resp = self._session.get(self._url("/api/health"), timeout=5)
            return resp.ok
        except requests.RequestException:
            return False
