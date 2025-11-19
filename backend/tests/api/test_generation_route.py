"""Tests for the /generate-materials endpoint."""
from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from agents import GeneratedBundle
from api.routes import generation as generation_route


@pytest.fixture
def fastapi_app():
    from app.main import app

    app.dependency_overrides.clear()
    yield app
    app.dependency_overrides.clear()


def test_generate_materials_success(fastapi_app) -> None:
    mock_agent = AsyncMock()
    mock_agent.generate_all.return_value = GeneratedBundle(
        cv="# Tailored CV",
        cover_letter="Dear Hiring Manager...",
        networking="Ask about scaling...",
        insights='{"score": 85}',
        match_score=85,
        generated_at=datetime.now(timezone.utc),
    )

    fastapi_app.dependency_overrides[generation_route.get_generation_agent] = lambda: mock_agent

    client = TestClient(fastapi_app)
    payload = {
        "job": {
            "id": "123",
            "title": "Dev",
            "company": "Corp",
            "description": "Code stuff",
            "skills": ["Python"]
        },
        "profile": {
            "cvText": "My CV content"
        }
    }
    
    response = client.post("/generate-materials", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["cv"] == "# Tailored CV"
    assert data["matchScore"] == 85
    assert data["jobId"] == "123"
