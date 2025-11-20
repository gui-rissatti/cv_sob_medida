"""LLM-powered extraction agent that normalizes scraped job content."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from textwrap import shorten
from typing import Iterable

import structlog
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, Field

from core.validators import JobValidator, ValidationError
from services.scraper import ScrapedJob

try:  # pragma: no cover - optional dependency wiring
    from langchain_google_genai import ChatGoogleGenerativeAI  # type: ignore
except Exception:  # pragma: no cover - module might be unavailable in tests
    ChatGoogleGenerativeAI = None  # type: ignore[misc]


LOGGER = structlog.get_logger(__name__)


@dataclass(slots=True)
class ExtractionAgentResult:
    """Represents the structured output coming from the LLM pipeline."""

    job: ScrapedJob
    highlights: list[str]


class _StructuredJobPayload(BaseModel):
    title: str = Field(..., description="Canonical job title")
    company: str = Field(..., description="Canonical employer name")
    description: str = Field(..., description="Concise but detailed responsibilities and requirements")
    skills: list[str] = Field(default_factory=list, description="Sorted, deduplicated skills")
    highlights: list[str] = Field(default_factory=list, description="Key bullet points extracted from the posting")


class ExtractionAgentError(RuntimeError):
    """Raised when the extraction agent cannot produce a structured job."""


class ExtractionAgent:
    """Pipeline that feeds scraped HTML/content into a Gemini-backed LangChain chain."""

    def __init__(
        self,
        *,
        llm: RunnableSerializable | None = None,
        validator: JobValidator | None = None,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.2,
        highlight_count: int = 3,
    ) -> None:
        self._validator = validator or JobValidator()
        self._highlight_count = highlight_count
        self._parser = PydanticOutputParser(pydantic_object=_StructuredJobPayload)
        self._prompt = self._build_prompt()
        self._llm = llm or self._build_default_llm(model=model, temperature=temperature)
        self._chain = self._prompt | self._llm | self._parser

    async def run(self, scraped_job: ScrapedJob) -> ExtractionAgentResult:
        """Normalize a scraped job using the LLM and return merged results."""

        LOGGER.debug("extraction_agent.run.start", board=scraped_job.board, url=scraped_job.url)
        validated = self._validated(scraped_job)
        prompt_input = self._prompt_input(validated)
        try:
            structured: _StructuredJobPayload = await self._chain.ainvoke(prompt_input)
        except Exception as exc:  # pragma: no cover - langchain surfaces various runtime errors
            raise ExtractionAgentError("LLM extraction failed") from exc

        merged_job = self._merge_payload(validated, structured)
        final_job = self._validated(merged_job)
        LOGGER.debug("extraction_agent.run.success", board=final_job.board, url=final_job.url)
        return ExtractionAgentResult(job=final_job, highlights=structured.highlights)

    def _validated(self, job: ScrapedJob) -> ScrapedJob:
        try:
            return self._validator.validate(job)
        except ValidationError as exc:
            # Provide detailed validation issues to help diagnose problems
            error_details = "\n".join(f"  - {issue.field}: {issue.message}" for issue in exc.issues)
            raise ExtractionAgentError(f"Validation failed for scraped job:\n{error_details}") from exc

    def _merge_payload(self, original: ScrapedJob, structured: _StructuredJobPayload) -> ScrapedJob:
        skills = structured.skills or original.skills
        deduped_skills = self._dedupe(skills)
        return ScrapedJob(
            url=original.url,
            board=original.board,
            title=structured.title or original.title,
            company=structured.company or original.company,
            description=structured.description or original.description,
            skills=deduped_skills,
            raw_html=original.raw_html,
        )

    def _prompt_input(self, job: ScrapedJob) -> dict[str, object]:
        job_dict = asdict(job)
        return {
            "job_data": job_dict,
            "job_html_preview": self._html_preview(job.raw_html),
            "format_instructions": self._parser.get_format_instructions(),
            "highlight_count": self._highlight_count,
        }

    def _build_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert technical recruiter. Transform scraped job postings into a structured, "
                    "clean summary with consistent casing and deduplicated skills. Only use the provided "
                    "content; never invent employers or titles. Return JSON that matches the provided format instructions.",
                ),
                (
                    "human",
                    "Job data: {job_data}\n\nHTML snippet:\n{job_html_preview}\n\n"
                    "You must respond with JSON using the following schema instructions:\n{format_instructions}\n"
                    "Generate up to {highlight_count} concise highlights describing the opportunity.",
                ),
            ]
        )

    def _build_default_llm(self, *, model: str, temperature: float) -> RunnableSerializable:
        if ChatGoogleGenerativeAI is None:
            raise ExtractionAgentError(
                "ChatGoogleGenerativeAI is unavailable. Provide an LLM instance when instantiating ExtractionAgent."
            )
        from core.config import get_settings
        settings = get_settings()
        return ChatGoogleGenerativeAI(
            model=model, 
            temperature=temperature, 
            convert_system_message_to_human=True,
            google_api_key=settings.google_api_key
        )

    @staticmethod
    def _html_preview(html: str, limit: int = 2000) -> str:
        return shorten(html, width=limit, placeholder=" …") if html else ""

    @staticmethod
    def _dedupe(values: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        unique: list[str] = []
        for value in values:
            normalized = value.strip()
            if not normalized:
                continue
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(normalized)
        return unique


__all__ = ["ExtractionAgent", "ExtractionAgentError", "ExtractionAgentResult"]
