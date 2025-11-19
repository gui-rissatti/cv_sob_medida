"""Pytest configuration and shared fixtures."""
from __future__ import annotations

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv


def _load_env_file() -> None:
    """Load .env from backend root if present, fallback to environment."""
    backend_root = Path(__file__).resolve().parents[1]
    env_file = backend_root / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    else:
        load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def load_env() -> None:
    """Ensure environment variables are available for every test session."""
    _load_env_file()


@pytest.fixture(scope="session")
def require_gemini_key() -> None:
    """Skip integration tests when GOOGLE_API_KEY is missing."""
    if not os.getenv("GOOGLE_API_KEY"):
        pytest.skip(
            "GOOGLE_API_KEY não configurada. "
            "Crie backend/.env com sua chave da Google antes de executar testes."
        )
