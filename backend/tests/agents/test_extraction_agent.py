"""Tests for the ExtractionAgent that wraps the LangChain pipeline."""
from __future__ import annotations

import pytest
from langchain_core.runnables import RunnableLambda

from agents import ExtractionAgent, ExtractionAgentError
from services.scraper import ScrapedJob


@pytest.fixture
def scraped_job() -> ScrapedJob:
    return ScrapedJob(
        url="https://www.linkedin.com/jobs/view/123",
        board="linkedin",
        title="Sr. Backend Dev",
        company="Example Corp",
        description=(
            "We are looking for an engineer to build APIs, improve data pipelines, and lead reliability initiatives. "
            "Experience with FastAPI, SQL, and observability platforms is desired."
        ),
        skills=["Python", "FastAPI", "SQL"],
        raw_html="<html><body><h1>Sr. Backend Dev</h1></body></html>",
    )


LONG_DESCRIPTION = (
    "Design reliable backend services, collaborate with cross-functional partners, ensure observability, "
    "and drive continuous improvements across distributed systems and developer tooling."
)


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_extraction_agent_returns_structured_job(scraped_job: ScrapedJob, anyio_backend: str) -> None:
    fake_response = (
        '{"title": "Senior Backend Engineer", "company": "Example Corp", "description": '
        f'"{LONG_DESCRIPTION}", "skills": ["Python", "FastAPI", "SQL"], "highlights": '
        '["Lead backend initiatives", "Scale APIs"]}'
    )
    agent = ExtractionAgent(llm=RunnableLambda(lambda _: fake_response))

    result = await agent.run(scraped_job)

    assert result.job.title == "Senior Backend Engineer"
    assert result.job.company == "Example Corp"
    assert result.job.skills == ["Python", "FastAPI", "SQL"]
    assert result.highlights == ["Lead backend initiatives", "Scale APIs"]


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_extraction_agent_falls_back_to_original_fields_when_missing(scraped_job: ScrapedJob, anyio_backend: str) -> None:
    fake_response = (
        '{"title": "", "company": "", "description": "", '
        '"skills": [], "highlights": []}'
    )
    agent = ExtractionAgent(llm=RunnableLambda(lambda _: fake_response))

    result = await agent.run(scraped_job)

    assert result.job.title == scraped_job.title
    assert result.job.company == scraped_job.company
    assert result.job.skills == scraped_job.skills
    assert result.job.description == scraped_job.description


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_extraction_agent_raises_when_parser_fails(scraped_job: ScrapedJob, anyio_backend: str) -> None:
    agent = ExtractionAgent(llm=RunnableLambda(lambda _: "not-json"))

    with pytest.raises(ExtractionAgentError):
        await agent.run(scraped_job)
