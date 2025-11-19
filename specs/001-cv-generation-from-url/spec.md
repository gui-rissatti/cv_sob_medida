# Feature Spec — CV Generation from URL

## Overview
Build an end-to-end experience where candidates paste a job URL and receive a customized application kit (CV, cover letter, networking tips, actionable insights) plus a searchable local history. The system must enforce test-first and contracts-first development, use FastAPI + LangChain (Google Gemini 1.5 Pro), and meet strict quality/deploy gates.

## Goals & Non-Goals
- **Goals**: Reliable job extraction (>90% on LinkedIn/Gupy/Indeed), fast material generation (<30s), complete candidate history with IndexedDB, CI/CD with zero-downtime deploy (Vercel + Render/Railway).
- **Non-Goals**: Building authentication, payment/credits, or admin tooling in this iteration.

## Personas
- **Candidate**: Pastes job URLs, receives tailored materials, expects PDF export and history.
- **Developer**: Needs automated deploy, observability, and guardrails.

## User Stories & Acceptance Criteria

### US1 — Extração de Vagas
- Paste URL → system extracts structured Job data.
- **Acceptance**:
  - >90% extraction success for LinkedIn, Gupy, Indeed.
  - Validation stack (syntax, semantics, completeness) rejects malformed data.
  - Response in <5s p95.

### US2 — Geração de Materiais
- Using job data + CV input, generate CV, cover letter, networking plan, insights.
- **Acceptance**:
  - 4 assets generated <30s total.
  - Match score >70% before returning payload.
  - CV & cover letter downloadable as PDF.

### US3 — Interface de Usuário
- React UI for URL input, CV paste, results, and PDF export.
- **Acceptance**:
  - Responsive layout desktop/mobile.
  - Clear loading/error states.
  - Copy-to-clipboard + PDF export available.

### US4 — Histórico e Persistência
- View/search/export application history stored locally via IndexedDB.
- **Acceptance**:
  - Entries automatically saved client-side with company, title, timestamp.
  - Search by company/title; export entire history JSON.

### US5 — Deploy & Observability
- Fully automated CI/CD with health checks and rollback.
- **Acceptance**:
  - GitHub Actions pipeline running lint, type-check, tests, coverage >70%.
  - Health checks `/health`, root.
  - Structured JSON logs + metrics.
  - README + .env.example documenting all variables.

## Functional Requirements
- FastAPI backend with endpoints `/extract-job-details`, `/generate-materials`, `/generate-complete`, `/health` per OpenAPI.
- WebScraperService w/ httpx, BeautifulSoup, Tenacity retries, fallback parsing.
- ExtractionAgent & GenerationAgent via LangChain calling Google Gemini 1.5 Pro and LangSmith tracing.
- Compatibility scoring service (0–100) gating responses.
- React 19 + Vite + Tailwind UI with Zustand global store, jsPDF/pdf-lib exports, IndexedDB wrapper.
- History sidebar with filters and export.

## Non-Functional Requirements
- Performance: API <5s p95, generation <30s, frontend FCP <3s.
- Availability: 99.5% uptime, zero-downtime deploy with health checks + automatic rollback.
- Security: HTTPS, rate limiting 10 req/min/IP, input sanitization, secure secrets.
- Observability: Structlog JSON logs, LangSmith traces, metrics for latency and success rate.

## Technical Constraints & Stack
- Backend: FastAPI 0.104+, Python 3.11, LangChain 0.1+, LangSmith, Google Gemini 1.5 Pro, BeautifulSoup4, httpx, Structlog, Tenacity.
- Frontend: React 19.2, TypeScript 5.8 (strict), Vite 6.2, Tailwind CSS, jsPDF + pdf-lib, IndexedDB.
- DevOps: Docker, GitHub Actions, Vercel (frontend), Render/Railway (backend).

## Success Metrics
1. Extraction success rate ≥90% for targeted job boards.
2. Match score ≥70% on generated kits.
3. Coverage ≥70%, lint/type checks green, integration tests hitting real Gemini when key present.
4. Health checks returning 200 OK in all environments.
5. Automated deploy completes with zero downtime and rollback plan.

## Open Questions
1. Job board priority beyond LinkedIn/Gupy/Indeed (tracked in `research.md`).
2. Rate limits per user vs IP (initially 10 req/min/IP).
3. PDF generation approach (decided: client-side via jsPDF/pdf-lib).
