from __future__ import annotations
from pathlib import Path
from urllib.parse import urljoin
import os


def _get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


BASE_URL = _get_env("BASE_URL", "https://<your-app-host>")
APP_ROOT = _get_env("APP_ROOT", "")


def base_url() -> str:
    """
    Return the base application URL used to start browser sessions.
    """
    return BASE_URL.rstrip("/")


def url(path: str = "/") -> str:
    """
    Build a fully qualified application URL from a relative path.

    Examples:
        url("/dashboard/") -> "https://<your-app-host>/dashboard/"
        url("/salesdata/") -> "https://<your-app-host>/salesdata/"
    """
    return urljoin(f"{base_url()}/", path.lstrip("/"))


def project_root() -> Path:
    """
    Return the repository root as a Path.
    """
    return Path(__file__).resolve().parent.parent
