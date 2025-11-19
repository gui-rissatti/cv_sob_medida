"""End-to-end tests for the full user journey."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from langchain_core.runnables import RunnableLambda

from agents import ExtractionAgent, GeneratedBundle, GenerationAgent
from api.routes import extraction as extraction_route
from api.routes import generation as generation_route
from services.scraper import ScrapedJob


@pytest.fixture
def fastapi_app():
    from app.main import app

    app.dependency_overrides.clear()
    yield app
    app.dependency_overrides.clear()


class _MockScraper:
    async def fetch_job(self, url: str) -> ScrapedJob:
        return ScrapedJob(
            url=url,
            board="linkedin",
            title="Software Engineer",
            company="Tech Corp",
            description="Write code. " * 20,  # Ensure enough length for validation
            skills=["Python"],
            raw_html="<html>...</html>",
        )


def test_extraction_to_generation_flow(fastapi_app) -> None:
    """Simulate the user flow: Extract Job -> Generate Materials."""
    
    # 1. Setup Mocks
    
    # Extraction Agent Mock (LLM)
    extraction_llm_response = json.dumps({
        "title": "Software Engineer",
        "company": "Tech Corp",
        "description": "Write code. " * 20,
        "skills": ["Python"],
        "highlights": ["Great team"]
    })
    extraction_agent = ExtractionAgent(llm=RunnableLambda(lambda _: extraction_llm_response))
    
    # Generation Agent Mock (We mock the agent directly or its LLM? 
    # GenerationAgent uses multiple chains. Mocking the LLM is complex because it receives different prompts.
    # Easier to mock the GenerationAgent.generate_all method for this high-level test.)
    mock_generation_agent = AsyncMock(spec=GenerationAgent)
    mock_generation_agent.generate_all.return_value = GeneratedBundle(
        cv="# Tailored CV",
        cover_letter="Dear Hiring Manager...",
        networking="Connect with...",
        insights='{"score": 90, "strengths": ["Python"], "gap": "None"}',
        match_score=90,
        generated_at=datetime.now(timezone.utc),
    )

    # Override dependencies
    fastapi_app.dependency_overrides[extraction_route.get_scraper_service] = lambda: _MockScraper()
    fastapi_app.dependency_overrides[extraction_route.get_extraction_agent] = lambda: extraction_agent
    fastapi_app.dependency_overrides[generation_route.get_generation_agent] = lambda: mock_generation_agent

    client = TestClient(fastapi_app)

    # 2. Execute Extraction
    extract_resp = client.post("/extract-job-details", json={"url": "https://linkedin.com/jobs/123"})
    assert extract_resp.status_code == 200
    job_data = extract_resp.json()
    
    assert job_data["title"] == "Software Engineer"
    assert job_data["id"] is not None

    # 3. Execute Generation (using data from extraction)
    generate_payload = {
        "job": {
            "id": job_data["id"],
            "title": job_data["title"],
            "company": job_data["company"],
            "description": job_data["description"],
            "skills": job_data["skills"]
        },
        "profile": {
            "cvText": "I know Python."
        }
    }
    
    gen_resp = client.post("/generate-materials", json=generate_payload)
    assert gen_resp.status_code == 200
    materials = gen_resp.json()
    
    assert materials["cv"] == "# Tailored CV"
    assert materials["matchScore"] == 90
    assert materials["jobId"] == job_data["id"]
