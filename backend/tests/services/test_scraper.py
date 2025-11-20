"""Tests for the WebScraperService implementation."""
from __future__ import annotations

import httpx
import pytest

from services.scraper import (
    FetchError,
    ParseError,
    UnsupportedJobBoardError,
    WebScraperService,
)


def _mock_client(response_text: str, status: int = 200) -> httpx.AsyncClient:
    """Build a mock HTTP client that always returns the provided payload."""

    def _handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status_code=status, text=response_text)

    transport = httpx.MockTransport(_handler)
    return httpx.AsyncClient(transport=transport)


@pytest.mark.anyio
async def test_fetch_job_linkedin_parses_expected_fields() -> None:
    html = """
    <html>
      <body>
        <h1 class="top-card-layout__title">Senior Backend Engineer</h1>
        <a class="topcard__org-name-link">Tech Corp</a>
        <div class="description__text">
          <p>Build reliable APIs.</p>
          <p>Scale asynchronous systems.</p>
        </div>
        <ul class="description__job-criteria-list">
          <li class="description__job-criteria-item">Python</li>
          <li class="description__job-criteria-item">FastAPI</li>
        </ul>
      </body>
    </html>
    """
    async with _mock_client(html) as client:
        service = WebScraperService(client=client)
        job = await service.fetch_job("https://www.linkedin.com/jobs/view/123")

    assert job.board == "linkedin"
    assert job.title == "Senior Backend Engineer"
    assert job.company == "Tech Corp"
    assert "Build reliable APIs." in job.description
    assert job.skills == ["Python", "FastAPI"]


@pytest.mark.anyio
async def test_fetch_job_gupy_parses_expected_fields() -> None:
    html = """
    <html>
      <body>
        <h1 class="job-header__title">Product Designer</h1>
        <span class="job-header__company">Gupy</span>
        <section id="job-description">
          <p>Prototype new flows.</p>
          <p>Partner with research.</p>
        </section>
        <ul class="job-requirements__list">
          <li class="job-requirements__item">Figma</li>
          <li class="job-requirements__item">UX Research</li>
        </ul>
      </body>
    </html>
    """
    async with _mock_client(html) as client:
        service = WebScraperService(client=client)
        job = await service.fetch_job("https://portal.gupy.io/job/456")

    assert job.board == "gupy"
    assert job.title == "Product Designer"
    assert job.company == "Gupy"
    assert job.skills == ["Figma", "UX Research"]


@pytest.mark.anyio
async def test_fetch_job_indeed_parses_expected_fields() -> None:
    html = """
    <html>
      <body>
        <h1 class="jobsearch-JobInfoHeader-title">Data Engineer</h1>
        <div class="jobsearch-InlineCompanyRating">Indeed Corp</div>
        <div id="jobDescriptionText">
          <p>Maintain ETL pipelines.</p>
          <p>Champion observability.</p>
        </div>
        <div class="jobsearch-ReqAndQualSection-item">SQL</div>
        <div class="jobsearch-ReqAndQualSection-item">AWS</div>
      </body>
    </html>
    """
    async with _mock_client(html) as client:
        service = WebScraperService(client=client)
        job = await service.fetch_job("https://br.indeed.com/viewjob?jk=789")

    assert job.board == "indeed"
    assert job.title == "Data Engineer"
    assert job.company == "Indeed Corp"
    assert job.skills == ["SQL", "AWS"]


@pytest.mark.anyio
async def test_fetch_job_unsupported_domain_uses_generic_parser() -> None:
    html = """
    <html>
        <head><title>Software Engineer at TechCorp</title></head>
        <body>
            <div>We're hiring a Software Engineer to join our team...</div>
        </body>
    </html>
    """
    async with _mock_client(html) as client:
        service = WebScraperService(client=client)
        job = await service.fetch_job("https://example.com/jobs/1")
        assert job.board == "generic"
        assert job.url == "https://example.com/jobs/1"


@pytest.mark.anyio
async def test_fetch_job_wraps_http_errors() -> None:
    async with _mock_client("boom", status=500) as client:
        service = WebScraperService(client=client)
        with pytest.raises(FetchError):
            await service.fetch_job("https://www.linkedin.com/jobs/view/500")


@pytest.mark.anyio
async def test_fetch_job_raises_for_missing_required_fields() -> None:
    html = """
    <html>
      <body>
        <h1>Untitled</h1>
        <div class="description__text">No company tag present.</div>
      </body>
    </html>
    """
    async with _mock_client(html) as client:
        service = WebScraperService(client=client)
        with pytest.raises(ParseError):
            await service.fetch_job("https://www.linkedin.com/jobs/view/111")
