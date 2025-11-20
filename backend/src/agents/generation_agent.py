"""Agent for generating application materials using LLMs."""
from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import structlog
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSerializable
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

    async def generate_all(
        self, 
        job_data: dict[str, Any], 
        cv_text: str,
        language: str = "auto",
        tone: str = "professional",
        variance: int = 3,
    ) -> GeneratedBundle:
        """Generate all materials in parallel."""
        
        LOGGER.info("generation_agent.start", job_title=job_data.get("title"), language=language, tone=tone, variance=variance)

        # Detect language if auto
        target_language = self._resolve_language(job_data.get("description", ""), language)
        
        # Prepare inputs for chains
        inputs = {
            "job_title": job_data.get("title", ""),
            "job_company": job_data.get("company", ""),
            "job_description": job_data.get("description", ""),
            "job_skills": ", ".join(job_data.get("skills", [])),
            "candidate_cv": cv_text,
            "target_language": target_language,
            "tone": tone,
            "variance_level": variance,
        }

        # Define runnables
        cv_chain = CV_GENERATION_PROMPT | self._llm | self._str_parser
        cl_chain = COVER_LETTER_PROMPT | self._llm | self._str_parser
        net_chain = NETWORKING_PROMPT | self._llm | self._str_parser
        insights_chain = INSIGHTS_PROMPT | self._llm | self._str_parser

        # Execute in parallel
        # We use return_exceptions=False to fail fast if one fails, or handle individually?
        # For now, let's fail if any fails.
        results = await asyncio.gather(
            self._run_with_retry(cv_chain, inputs),
            self._run_with_retry(cl_chain, inputs),
            self._run_with_retry(net_chain, inputs),
            self._run_with_retry(insights_chain, inputs),
        )

        cv_result, cl_result, net_result, insights_text = results
        
        # Debug logging to ensure correct assignment
        LOGGER.debug("generation_agent.results", 
                    cv_start=cv_result[:50] if cv_result else "empty",
                    cl_start=cl_result[:50] if cl_result else "empty",
                    net_start=net_result[:50] if net_result else "empty",
                    insights_start=insights_text[:50] if insights_text else "empty")

        # Extract score from insights text
        llm_score = self._extract_score_from_insights(insights_text)
        
        # Fallback to heuristic if extraction fails
        if llm_score == 0:
            heuristic_score = calculate_heuristic_score(job_data.get("skills", []), cv_text)
            llm_score = heuristic_score
            LOGGER.warning("generation_agent.score_extraction_failed", using_heuristic=heuristic_score)
        else:
            heuristic_score = calculate_heuristic_score(job_data.get("skills", []), cv_text)
            LOGGER.debug("generation_agent.scores", llm=llm_score, heuristic=heuristic_score)

        return GeneratedBundle(
            cv=cv_result,
            cover_letter=cl_result,
            networking=net_result,
            insights=insights_text,  # Now storing formatted text instead of JSON
            match_score=llm_score,
            generated_at=datetime.now(timezone.utc),
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _run_with_retry(self, chain: RunnableSerializable, inputs: dict[str, Any]) -> Any:
        return await chain.ainvoke(inputs)

    def _extract_score_from_insights(self, insights_text: str) -> int:
        """Extract compatibility score from formatted insights text."""
        # Look for patterns like "Compatibilidade: 85/100" or "Compatibility: 85/100"
        patterns = [
            r"Compatibilidade:\s*(\d+)/100",
            r"Compatibility:\s*(\d+)/100",
            r"Compatibilité:\s*(\d+)/100",
            r"Compatibilidad:\s*(\d+)/100",
            r"##\s*\w+:\s*(\d+)/100",  # Generic heading with score
        ]
        
        for pattern in patterns:
            match = re.search(pattern, insights_text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return max(0, min(100, score))  # Clamp to 0-100
        
        return 0  # Return 0 if no score found

    def _resolve_language(self, description: str, language: str) -> str:
        """Detect or return the target language for outputs."""
        if language != "auto":
            return language
        
        # Simple heuristic: check for common words
        desc_lower = description.lower()
        
        # Portuguese indicators
        if any(word in desc_lower for word in ["você", "será", "responsável", "conhecimento", "experiência"]):
            return "pt"
        
        # Spanish indicators  
        if any(word in desc_lower for word in ["usted", "será", "responsable", "conocimiento", "experiencia"]):
            return "es"
        
        # French indicators
        if any(word in desc_lower for word in ["vous", "serez", "responsable", "connaissance", "expérience"]):
            return "fr"
        
        # Default to English
        return "en"
    
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
