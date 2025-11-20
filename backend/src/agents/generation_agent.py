"""Agent for generating application materials using LLMs."""
from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import structlog
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnableSerializable
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from core.scoring import calculate_heuristic_score
from prompts import (
    COVER_LETTER_PROMPT,
    CV_GENERATION_PROMPT,
    INSIGHTS_PROMPT,
    NETWORKING_PROMPT,
)

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None  # type: ignore

LOGGER = structlog.get_logger(__name__)


class InsightsResult(BaseModel):
    """Structured output for the insights generation."""

    score: int = Field(..., description="Compatibility score (0-100)")
    strengths: list[str] = Field(..., description="Key strengths to emphasize")
    gap: str = Field(..., description="Potential gap or weakness to address")


@dataclass(slots=True)
class GeneratedBundle:
    """Container for all generated assets."""

    cv: str
    cover_letter: str
    networking: str
    insights: str
    match_score: int
    generated_at: datetime


class GenerationAgent:
    """Orchestrates the generation of CVs, cover letters, and insights."""

    def __init__(
        self,
        *,
        llm: RunnableSerializable | None = None,
        model: str = "gemini-2.5-flash",
        temperature: float = 0.4,
    ) -> None:
        self._llm = llm or self._build_default_llm(model=model, temperature=temperature)
        self._str_parser = StrOutputParser()
        self._json_parser = JsonOutputParser(pydantic_object=InsightsResult)

    async def generate_all(self, job_data: dict[str, Any], cv_text: str) -> GeneratedBundle:
        """Generate all materials in parallel."""
        
        LOGGER.info("generation_agent.start", job_title=job_data.get("title"))

        # Prepare inputs for chains
        inputs = {
            "job_title": job_data.get("title", ""),
            "job_company": job_data.get("company", ""),
            "job_description": job_data.get("description", ""),
            "job_skills": ", ".join(job_data.get("skills", [])),
            "candidate_cv": cv_text,
        }

        # Define runnables
        cv_chain = CV_GENERATION_PROMPT | self._llm | self._str_parser
        cl_chain = COVER_LETTER_PROMPT | self._llm | self._str_parser
        net_chain = NETWORKING_PROMPT | self._llm | self._str_parser
        insights_chain = INSIGHTS_PROMPT | self._llm | self._json_parser

        # Execute in parallel
        # We use return_exceptions=False to fail fast if one fails, or handle individually?
        # For now, let's fail if any fails.
        results = await asyncio.gather(
            self._run_with_retry(cv_chain, inputs),
            self._run_with_retry(cl_chain, inputs),
            self._run_with_retry(net_chain, inputs),
            self._run_with_retry(insights_chain, inputs),
        )

        cv_result, cl_result, net_result, insights_data = results

        # Fallback or merge score
        # We have a heuristic score we could use as a sanity check or fallback
        heuristic_score = calculate_heuristic_score(job_data.get("skills", []), cv_text)
        llm_score = insights_data.get("score", 0)
        
        # Simple logic: Average them or trust LLM? 
        # Let's trust LLM but log the difference.
        LOGGER.debug("generation_agent.scores", llm=llm_score, heuristic=heuristic_score)

        return GeneratedBundle(
            cv=cv_result,
            cover_letter=cl_result,
            networking=net_result,
            insights=json.dumps(insights_data), # Store as JSON string as per data model
            match_score=llm_score,
            generated_at=datetime.now(timezone.utc),
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _run_with_retry(self, chain: RunnableSerializable, inputs: dict[str, Any]) -> Any:
        return await chain.ainvoke(inputs)

    def _build_default_llm(self, *, model: str, temperature: float) -> RunnableSerializable:
        if ChatGoogleGenerativeAI is None:
            raise RuntimeError(
                "ChatGoogleGenerativeAI is unavailable. Install langchain-google-genai."
            )
        from core.config import get_settings
        settings = get_settings()
        return ChatGoogleGenerativeAI(
            model=model, 
            temperature=temperature,
            google_api_key=settings.google_api_key
        )
