"""Tests for application configuration handling."""
from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure environment variables do not leak between tests."""
    keys = ["ENVIRONMENT", "API_PORT", "LOG_LEVEL", "CORS_ORIGINS"]
    for key in keys:
        monkeypatch.delenv(key, raising=False)

    from core.config import reset_settings_cache

    reset_settings_cache()


def test_settings_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Defaults should match development expectations when no env vars supplied."""
    from core.config import get_settings

    settings = get_settings(cache=False)

    assert settings.environment == "development"
    assert settings.api_port == 8000
    assert settings.log_level == "INFO"
    assert "http://localhost:5173" in settings.cors_origins


def test_settings_loads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Environment variables should override defaults and split comma-separated origins."""
    monkeypatch.setenv("ENVIRONMENT", "production")
    monkeypatch.setenv("API_PORT", "9000")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv(
        "CORS_ORIGINS",
        "http://localhost:5173,https://app.example.com",
    )

    from core.config import get_settings

    settings = get_settings(cache=False)

    assert settings.environment == "production"
    assert settings.api_port == 9000
    assert settings.log_level == "DEBUG"
    assert settings.cors_origins == [
        "http://localhost:5173",
        "https://app.example.com",
    ]
