"""Prompt templates for generating application materials."""
from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

CV_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert CV writer and career strategist. Your goal is to rewrite a candidate's CV "
            "to perfectly align with a specific job description. "
            "Use professional Markdown formatting. "
            "Focus on achievements, relevant skills, and keywords from the job description. "
            "Do not invent experiences, but frame existing ones to match the role requirements.",
        ),
        (
            "human",
            "JOB DETAILS:\n"
            "Title: {job_title}\n"
            "Company: {job_company}\n"
            "Description: {job_description}\n"
            "Required Skills: {job_skills}\n\n"
            "CANDIDATE CV:\n{candidate_cv}\n\n"
            "Task: Generate a tailored CV in Markdown format.",
        ),
    ]
)

COVER_LETTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert career coach. Write a compelling, personalized cover letter for the candidate "
            "applying to the specified job. "
            "The tone should be professional, enthusiastic, and confident. "
            "Highlight why the candidate is a great fit based on the provided CV and job description.",
        ),
        (
            "human",
            "JOB DETAILS:\n"
            "Title: {job_title}\n"
            "Company: {job_company}\n"
            "Description: {job_description}\n\n"
            "CANDIDATE CV:\n{candidate_cv}\n\n"
            "Task: Write a cover letter.",
        ),
    ]
)

NETWORKING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a networking expert. Provide actionable networking advice for this specific job application. "
            "Generate:\n"
            "1. Two LinkedIn connection request templates (under 300 chars) for recruiters or hiring managers.\n"
            "2. Two smart questions to ask during an interview that demonstrate deep understanding of the role.",
        ),
        (
            "human",
            "JOB DETAILS:\n"
            "Title: {job_title}\n"
            "Company: {job_company}\n"
            "Description: {job_description}\n\n"
            "Task: Provide networking templates and interview questions.",
        ),
    ]
)

INSIGHTS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a hiring manager. Analyze the match between the candidate and the job. "
            "Provide:\n"
            "1. A compatibility score (0-100) based on skills and experience match.\n"
            "2. Three key strengths to emphasize in the application.\n"
            "3. One potential gap or weakness to address proactively.\n"
            "Output as a JSON object with keys: 'score', 'strengths', 'gap'.",
        ),
        (
            "human",
            "JOB DETAILS:\n"
            "Title: {job_title}\n"
            "Description: {job_description}\n"
            "Required Skills: {job_skills}\n\n"
            "CANDIDATE CV:\n{candidate_cv}\n\n"
            "Task: Analyze the match and provide insights in JSON.",
        ),
    ]
)
