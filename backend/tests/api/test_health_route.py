"""Ensure foundational API routes are registered."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_route_returns_status_ok() -> None:
    from app.main import app

    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
