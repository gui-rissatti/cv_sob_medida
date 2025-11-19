"""Integration tests for the extraction flow via the public API."""
from __future__ import annotations

import asyncio
import hashlib
import json
from datetime import datetime

import httpx
import pytest
from fastapi.testclient import TestClient
from langchain_core.runnables import RunnableLambda

from agents import ExtractionAgent
from api.routes import extraction as extraction_route
from services.scraper import WebScraperService


def _mock_async_client(expected_url: str, html: str) -> httpx.AsyncClient:
    def _handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == expected_url
        return httpx.Response(status_code=200, text=html)

    return httpx.AsyncClient(transport=httpx.MockTransport(_handler))


def _stable_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]


@pytest.fixture
def app_client():
    from app.main import app

    app.dependency_overrides.clear()
    client = TestClient(app)
    yield app, client
    app.dependency_overrides.clear()
    client.close()


_LINKEDIN_HTML = """
<html>
  <body>
    <h1 class="top-card-layout__title">Senior Backend Dev</h1>
    <a class="topcard__org-name-link">Tech Corp</a>
    <div class="description__text">
      <p>Design distributed systems that power millions of data points daily.</p>
      <p>Collaborate with cross-functional teams and ensure best practices.</p>
      <p>Champion observability and developer productivity in every sprint.</p>
    </div>
    <ul class="description__job-criteria-list">
      <li class="description__job-criteria-item">Python</li>
      <li class="description__job-criteria-item">FastAPI</li>
      <li class="description__job-criteria-item">SQL</li>
    </ul>
  </body>
</html>
"""


@pytest.mark.parametrize(
    "case",
    [
        {
            "name": "linkedin",
            "url": "https://www.linkedin.com/jobs/view/123",
            "html": _LINKEDIN_HTML,
            "llm_response": json.dumps(
                {
                    "title": "Principal Backend Engineer",
                    "company": "Tech Corp",
                    "description": (
                        "Lead the architecture of mission-critical APIs, own observability, mentor peers, and "
                        "drive continuous improvements across distributed services operating at scale."
                    ),
                    "skills": ["Python", "FastAPI", "SQL", "Observability"],
                    "highlights": ["Lead architecture", "Mentor engineers"],
                }
            ),
            "expected_title": "Principal Backend Engineer",
            "expected_company": "Tech Corp",
            "expected_skills": ["Python", "FastAPI", "SQL", "Observability"],
        }
    ],
    ids=lambda case: case["name"],
)
def test_extract_job_details_integration_flow(case, app_client) -> None:
    app, client = app_client
    mock_client = _mock_async_client(case["url"], case["html"])
    scraper = WebScraperService(client=mock_client)
    agent = ExtractionAgent(llm=RunnableLambda(lambda _: case["llm_response"]))

    app.dependency_overrides[extraction_route.get_scraper_service] = lambda: scraper
    app.dependency_overrides[extraction_route.get_extraction_agent] = lambda: agent

    response = client.post("/extract-job-details", json={"url": case["url"]})

    assert response.status_code == 200
    payload = response.json()

    assert payload["id"] == _stable_id(case["url"])
    assert payload["url"] == case["url"]
    assert payload["title"] == case["expected_title"]
    assert payload["company"] == case["expected_company"]
    assert payload["skills"] == case["expected_skills"]
    # createdAt must be ISO8601 compliant and recent
    created_at = datetime.fromisoformat(payload["createdAt"].replace("Z", "+00:00"))
    assert (datetime.now(created_at.tzinfo) - created_at).total_seconds() < 5

    asyncio.run(mock_client.aclose())