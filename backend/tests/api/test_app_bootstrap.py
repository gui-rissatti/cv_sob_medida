"""Bootstrap tests for FastAPI application setup."""
from __future__ import annotations

from fastapi import FastAPI


def test_app_instance_exposes_metadata() -> None:
    """Ensure app.main exposes a FastAPI instance with title and version."""
    from app.main import app  # Local import to ensure module is importable

    assert isinstance(app, FastAPI)
    assert app.title == "CV Sob Medida API"
    assert app.version == "0.1.0"
