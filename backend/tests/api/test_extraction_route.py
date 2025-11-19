"""API-level tests for the /extract-job-details endpoint."""
from __future__ import annotations

import hashlib
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from agents import ExtractionAgentError
from api.routes import extraction as extraction_route
from core.validators import ValidationIssue, ValidationError as JobValidationError
from services.scraper import (
    ParseError,
    ScrapedJob,
    ScraperError,
    UnsupportedJobBoardError,
)


@pytest.fixture
def fastapi_app():
    from app.main import app

    app.dependency_overrides.clear()
    yield app
    app.dependency_overrides.clear()


def _job_payload() -> ScrapedJob:
    return ScrapedJob(
        url="https://www.linkedin.com/jobs/view/123",
        board="linkedin",
        title="Senior Backend Engineer",
        company="Tech Corp",
        description="Build reliable APIs and scale distributed systems across regions.",
        skills=["Python", "FastAPI"],
        raw_html="<html></html>",
    )


class _StubScraper:
    def __init__(self, *, job: ScrapedJob | None = None, error: Exception | None = None) -> None:
        self._job = job
        self._error = error

    async def fetch_job(self, url: str) -> ScrapedJob:
        if self._error:
            raise self._error
        assert self._job is not None
        return self._job


class _StubAgent:
    def __init__(self, *, job: ScrapedJob | None = None, fail_with_validation: bool = False) -> None:
        self._job = job
        self._fail_with_validation = fail_with_validation

    async def run(self, scraped_job: ScrapedJob) -> SimpleNamespace:
        if self._fail_with_validation:
            issues = [
                ValidationIssue(layer="syntax", field="title", message="Title missing", code="missing_title"),
            ]
            validation_error = JobValidationError(issues)
            raise ExtractionAgentError("Validation failed for scraped job") from validation_error
        return SimpleNamespace(job=self._job or scraped_job)


def test_extract_job_details_returns_normalized_payload(fastapi_app) -> None:
    job = _job_payload()
    expected_id = hashlib.sha1(job.url.encode("utf-8")).hexdigest()[:12]

    fastapi_app.dependency_overrides[extraction_route.get_scraper_service] = lambda: _StubScraper(job=job)
    fastapi_app.dependency_overrides[extraction_route.get_extraction_agent] = lambda: _StubAgent(job=job)

    client = TestClient(fastapi_app)
    response = client.post("/extract-job-details", json={"url": job.url})

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == expected_id
    assert payload["url"] == job.url
    assert payload["title"] == job.title
    assert payload["company"] == job.company
    assert payload["skills"] == job.skills
    assert "createdAt" in payload


def test_extract_job_details_handles_unsupported_url(fastapi_app) -> None:
    fastapi_app.dependency_overrides[extraction_route.get_scraper_service] = lambda: _StubScraper(
        error=UnsupportedJobBoardError("Domain 'example.com' is not supported")
    )
    fastapi_app.dependency_overrides[extraction_route.get_extraction_agent] = lambda: _StubAgent()

    client = TestClient(fastapi_app)
    response = client.post("/extract-job-details", json={"url": "https://example.com/jobs/1"})

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"] == "unsupported_url"
    assert "example.com" in payload["message"]


def test_extract_job_details_surfaces_validation_details(fastapi_app) -> None:
    job = _job_payload()
    fastapi_app.dependency_overrides[extraction_route.get_scraper_service] = lambda: _StubScraper(job=job)
    fastapi_app.dependency_overrides[extraction_route.get_extraction_agent] = lambda: _StubAgent(
        job=job, fail_with_validation=True
    )

    client = TestClient(fastapi_app)
    response = client.post("/extract-job-details", json={"url": job.url})

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"] == "extraction_failed"
    assert payload["details"] == ["syntax.title: Title missing"]


def test_extract_job_details_handles_generic_scraper_error(fastapi_app) -> None:
    fastapi_app.dependency_overrides[extraction_route.get_scraper_service] = lambda: _StubScraper(
        error=ScraperError("network failure")
    )
    fastapi_app.dependency_overrides[extraction_route.get_extraction_agent] = lambda: _StubAgent()

    client = TestClient(fastapi_app)
    response = client.post("/extract-job-details", json={"url": "https://www.linkedin.com/jobs/view/123"})

    assert response.status_code == 500
    payload = response.json()
    assert payload["error"] == "scrape_failed"
    assert "network failure" in payload["message"]
