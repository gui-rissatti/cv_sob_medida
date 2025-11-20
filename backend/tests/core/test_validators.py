"""Unit tests for the validation layer that checks scraped jobs."""
from __future__ import annotations

import pytest

from core.validators import JobValidator, ValidationError
from services.scraper import ScrapedJob


def _make_job(**overrides: object) -> ScrapedJob:
    base = {
        "url": "https://www.linkedin.com/jobs/view/123",
        "board": "linkedin",
        "title": "Senior Backend Engineer",
        "company": "Tech Corp",
        "description": (
            "Build reliable APIs and services. "
            "Scale distributed systems while collaborating with product and data teams. "
            "Champion observability and developer experience improvements across the stack."
        ),
        "skills": ["Python", "FastAPI", "SQL"],
        "raw_html": "<html></html>",
    }
    base.update(overrides)
    return ScrapedJob(**base)


def test_job_validator_accepts_valid_payload() -> None:
    validator = JobValidator()
    job = _make_job()

    validated = validator.validate(job)

    assert validated.title == "Senior Backend Engineer"
    assert validated.company == "Tech Corp"
    assert validated.skills == ["Python", "FastAPI", "SQL"]


def test_validate_raises_for_invalid_url_format() -> None:
    validator = JobValidator()
    job = _make_job(url="notaurl")

    with pytest.raises(ValidationError) as excinfo:
        validator.validate(job)

    assert any(issue.layer == "syntax" and issue.field == "url" for issue in excinfo.value.issues)


def test_validate_rejects_unknown_board_semantically() -> None:
    validator = JobValidator()
    job = _make_job(board="github")

    with pytest.raises(ValidationError) as excinfo:
        validator.validate(job)

    assert any(issue.layer == "semantic" and issue.field == "board" for issue in excinfo.value.issues)


def test_validate_flags_incomplete_fields() -> None:
    validator = JobValidator(min_description_words=20, min_skill_count=1)
    job = _make_job(description="Short summary", skills=[])

    with pytest.raises(ValidationError) as excinfo:
        validator.validate(job)

    desc_issue = next(
        issue for issue in excinfo.value.issues if issue.field == "description" and issue.layer == "completeness"
    )
    skills_issue = next(
        issue for issue in excinfo.value.issues if issue.field == "skills" and issue.layer == "completeness"
    )
    assert "words" in desc_issue.message
    assert "skill" in skills_issue.message


def test_validator_normalizes_whitespace_and_deduplicates_skills() -> None:
    validator = JobValidator()
    job = _make_job(
        title="  Senior Backend Engineer  ",
        company="  Tech Corp  ",
        description="  Build APIs.  Lead teams.  Improve reliability.  "
        "This paragraph ensures we have enough content for validation.",
        skills=[" python ", "FastAPI", "PYTHON", "fastapi"],
    )

    validated = validator.validate(job)

    assert validated.title == "Senior Backend Engineer"
    assert validated.company == "Tech Corp"
    assert validated.skills == ["Python", "FastAPI"]


def test_validation_error_message_contains_issue_summary() -> None:
    validator = JobValidator()
    job = _make_job(url="notaurl", company="")

    with pytest.raises(ValidationError) as excinfo:
        validator.validate(job)

    message = str(excinfo.value)
    assert "company" in message
    assert "url" in message
