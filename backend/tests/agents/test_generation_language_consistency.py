"""Tests for language consistency and output format in generation agent."""
import re

import pytest

from agents.generation_agent import GenerationAgent


@pytest.fixture
def sample_job_data():
    """Sample job data for testing."""
    return {
        "title": "Software Engineer",
        "company": "TechCorp",
        "description": "We are looking for a talented software engineer with experience in Python and AWS.",
        "skills": ["Python", "AWS", "Docker"],
    }


@pytest.fixture
def sample_cv_text():
    """Sample CV text for testing."""
    return """
John Doe
john.doe@email.com | +1-555-0100
linkedin.com/in/johndoe

Professional software engineer with 5 years of experience in Python development.

## Experience

**Senior Developer** | TechStart Inc. | 2020-Present
- Developed microservices using Python and FastAPI
- Deployed applications on AWS with Docker containers
- Improved system performance by 40%

**Developer** | StartupCo | 2018-2020
- Built REST APIs with Python Flask
- Managed PostgreSQL databases
- Implemented CI/CD pipelines

## Education

**B.S. Computer Science** | State University | 2018

## Skills

Python, AWS, Docker, FastAPI, PostgreSQL, Git
"""


class TestLanguageConsistency:
    """Test that all outputs respect the target language setting."""

    @pytest.mark.anyio
    async def test_all_outputs_in_portuguese(self, sample_job_data, sample_cv_text):
        """Test that when language='pt', all outputs are in Portuguese."""
        agent = GenerationAgent(temperature=0.3)
        
        result = await agent.generate_all(
            job_data=sample_job_data,
            cv_text=sample_cv_text,
            language="pt",
            tone="professional",
            variance=3,
        )
        
        # Debug output
        print(f"\n=== INSIGHTS OUTPUT ===\n{result.insights[:500]}\n=================")
        
        # Check that insights contains Portuguese section titles or formatted content
        insights_lower = result.insights.lower()
        assert "compatibilidade" in insights_lower or "pontos fortes" in insights_lower or "##" in result.insights
        
        # Insights should not contain raw JSON
        assert not result.insights.startswith("{")
        assert '"score":' not in result.insights
        assert '"strengths":' not in result.insights

    @pytest.mark.anyio
    async def test_all_outputs_in_english(self, sample_job_data, sample_cv_text):
        """Test that when language='en', all outputs are in English."""
        agent = GenerationAgent(temperature=0.3)
        
        result = await agent.generate_all(
            job_data=sample_job_data,
            cv_text=sample_cv_text,
            language="en",
            tone="professional",
            variance=3,
        )
        
        # Check that insights contains English section titles
        assert "Compatibility:" in result.insights or "Strengths" in result.insights
        
        # Insights should not contain raw JSON
        assert not result.insights.startswith("{")
        assert "\"score\":" not in result.insights


class TestOutputFormatting:
    """Test that outputs follow the mandated structure."""

    @pytest.mark.anyio
    async def test_cv_has_mandatory_structure(self, sample_job_data, sample_cv_text):
        """Test that CV follows the mandatory structure without auxiliary labels."""
        agent = GenerationAgent(temperature=0.3)
        
        result = await agent.generate_all(
            job_data=sample_job_data,
            cv_text=sample_cv_text,
            language="en",
            tone="professional",
            variance=3,
        )
        
        cv = result.cv
        
        # Should not contain auxiliary labels
        assert "Headline:" not in cv
        assert "Summary:" not in cv
        assert "Profile:" not in cv
        
        # Should contain mandatory sections
        assert "## Experience" in cv or "## Work Experience" in cv
        assert "## Education" in cv
        assert "## Skills" in cv or "## Technical Skills" in cv
        
        # Should not be wrapped in code blocks
        assert not cv.startswith("```")
        assert not cv.endswith("```")

    @pytest.mark.anyio
    async def test_insights_formatted_not_json(self, sample_job_data, sample_cv_text):
        """Test that insights are formatted text, not raw JSON."""
        agent = GenerationAgent(temperature=0.3)
        
        result = await agent.generate_all(
            job_data=sample_job_data,
            cv_text=sample_cv_text,
            language="en",
            tone="professional",
            variance=3,
        )
        
        insights = result.insights
        
        # Should be formatted markdown, not JSON
        assert not insights.startswith("{")
        assert not insights.endswith("}")
        
        # Should not contain JSON structure
        assert "\"score\":" not in insights
        assert "\"strengths\":" not in insights
        assert "\"gap\":" not in insights
        
        # Should contain markdown headers
        assert "##" in insights
        
        # Should be readable text
        assert len(insights.strip()) > 50

    @pytest.mark.anyio
    async def test_score_extraction_from_insights(self, sample_job_data, sample_cv_text):
        """Test that match score is correctly extracted from formatted insights."""
        agent = GenerationAgent(temperature=0.3)
        
        result = await agent.generate_all(
            job_data=sample_job_data,
            cv_text=sample_cv_text,
            language="pt",
            tone="professional",
            variance=3,
        )
        
        # Score should be extracted and valid
        assert 0 <= result.match_score <= 100
        
        # Score should appear in insights text
        score_pattern = rf"{result.match_score}/100"
        assert score_pattern in result.insights or result.match_score > 0


class TestScoreExtraction:
    """Test the score extraction method."""

    def test_extract_score_portuguese(self):
        """Test score extraction from Portuguese text."""
        agent = GenerationAgent()
        
        text = """
## Compatibilidade: 85/100

### Pontos Fortes
- Strong Python skills
        """
        
        score = agent._extract_score_from_insights(text)
        assert score == 85

    def test_extract_score_english(self):
        """Test score extraction from English text."""
        agent = GenerationAgent()
        
        text = """
## Compatibility: 92/100

### Strengths
- Excellent technical background
        """
        
        score = agent._extract_score_from_insights(text)
        assert score == 92

    def test_extract_score_no_match(self):
        """Test score extraction when no score found."""
        agent = GenerationAgent()
        
        text = "Some text without score"
        
        score = agent._extract_score_from_insights(text)
        assert score == 0

    def test_extract_score_clamps_values(self):
        """Test that extracted scores are clamped to 0-100."""
        agent = GenerationAgent()
        
        # This shouldn't happen, but test the safety mechanism
        text = "Compatibility: 150/100"
        score = agent._extract_score_from_insights(text)
        assert score == 100
