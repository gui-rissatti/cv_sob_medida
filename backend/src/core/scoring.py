"""Compatibility scoring logic for job applications."""
from __future__ import annotations

import re


def calculate_heuristic_score(job_skills: list[str], cv_text: str) -> int:
    """
    Calculate a baseline compatibility score (0-100) based on skill presence in the CV.

    This is a simple heuristic that checks for the existence of job skills in the CV text.
    It is case-insensitive.
    """
    if not job_skills:
        return 0

    cv_lower = cv_text.lower()
    match_count = 0

    for skill in job_skills:
        # Simple substring match, could be improved with regex for word boundaries
        # Escaping skill to avoid regex errors if it contains special chars
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, cv_lower):
            match_count += 1

    if match_count == 0:
        return 0

    # Calculate percentage
    score = (match_count / len(job_skills)) * 100
    return min(int(score), 100)
