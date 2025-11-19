# Tasks: CV Generation from URL

**Input**: Design documents from `specs/001-cv-generation-from-url/`
**Prerequisites**: `plan.md`, `spec.md` (user stories from prompt), `research.md`, `data-model.md`, `contracts/`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`
- **Shared**: `shared/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend.

- [X] T001 Create project structure: `backend/`, `frontend/`, `shared/` directories.
- [X] T002 [P] Initialize FastAPI project in `backend/` with `main.py` and `pyproject.toml`.
- [X] T003 [P] Initialize Vite+React+TS project in `frontend/` using `npm create vite@latest frontend -- --template react-ts`.
- [X] T004 [P] Configure linting (ESLint) and formatting (Prettier) for `frontend/`.
- [X] T005 [P] Configure linting (Ruff) and formatting (Black) for `backend/`.
- [X] T006 Define shared types from `data-model.md` in `shared/types.ts`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [X] T007 [P] **Backend**: Setup API routing structure in `backend/src/api/`.
- [X] T008 [P] **Backend**: Implement logging configuration using `structlog` in `backend/src/core/logging.py`.
- [X] T009 [P] **Backend**: Configure environment variable handling (e.g., using Pydantic's `BaseSettings`) in `backend/src/core/config.py`.
- [X] T010 [P] **Frontend**: Setup project structure with `components/`, `services/`, `hooks/`, `pages/` directories in `frontend/src/`.
- [X] T011 [P] **Frontend**: Configure Tailwind CSS in `frontend/`.
- [X] T012 **DevOps**: Create initial `docker-compose.yml` to run backend and frontend services.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Extração de Vagas (Priority: P1) 🎯 MVP

**Goal**: As a candidate, I want to paste a job URL and receive its extracted details.
**Independent Test**: Make a POST request to `/extract-job-details` with a supported URL and verify the returned JSON matches the `Job` schema from `data-model.md`.

### Implementation for User Story 1

- [X] T013 [US1] Create `contracts/extraction-api.yaml` with the OpenAPI spec for the `/extract-job-details` endpoint.
- [X] T014 [US1] Write contract tests for `/extract-job-details` based on `extraction-api.yaml` in `backend/tests/contract/test_extraction.py`.
- [X] T015 [US1] Implement `WebScraperService` with `httpx` and `BeautifulSoup4` in `backend/src/services/scraper.py`.
- [X] T016 [P] [US1] Implement multi-layer validation (syntax, semantic, completeness) for scraped data in `backend/src/core/validators.py`.
- [X] T017 [US1] Create `ExtractionAgent` using LangChain to process and structure scraped content in `backend/src/agents/extraction_agent.py`.
- [X] T018 [US1] Implement the `/extract-job-details` endpoint in `backend/src/api/endpoints/extraction.py`.
- [X] T019 [US1] Write integration tests for the extraction flow using real job board URLs in `backend/tests/integration/test_extraction_flow.py`.

**Checkpoint**: Backend extraction is functional with a high success rate.

---

## Phase 4: User Story 2 - Geração de Materiais (Priority: P2)

**Goal**: As a candidate, I want to receive a full set of application materials for a job.
**Independent Test**: Make a POST request to `/generate-materials` with job details and a CV, and verify the generated assets are returned.

### Implementation for User Story 2

- [X] T020 [P] [US2] Create `contracts/generation-api.yaml` with specs for `/generate-materials` and `/generate-complete`.
- [X] T021 [US2] Write contract tests for `/generate-materials` in `backend/tests/contract/test_generation.py`.
- [X] T022 [US2] Implement structured prompts for CV, cover letter, networking, and tips in `backend/src/prompts/`.
- [X] T023 [P] [US2] Create a compatibility scoring system in `backend/src/core/scoring.py`.
- [X] T024 [US2] Create `GenerationAgent` with retry logic (`tenacity`) in `backend/src/agents/generation_agent.py`.
- [X] T025 [US2] Implement `/generate-materials` and `/generate-complete` endpoints in `backend/src/api/endpoints/generation.py`.
- [X] T026 [US2] Write E2E tests for the full extraction + generation flow in `backend/tests/e2e/test_full_flow.py`.

**Checkpoint**: Backend generation is functional with a response time under 30 seconds.

---

## Phase 5: User Story 3 - Interface de Usuário (Priority: P3)

**Goal**: As a candidate, I want a simple interface to input a URL and see the generated materials.
**Independent Test**: Open the web app, paste a URL, and see the generated CV, cover letter, etc., displayed correctly.

### Implementation for User Story 3

- [X] T027 [US3] Setup project with Vite, React, and TypeScript (already done in T003).
- [X] T028 [P] [US3] Create the `InputSection` component in `frontend/src/components/InputSection.tsx`.
- [X] T029 [P] [US3] Create the `OutputSection` component in `frontend/src/components/OutputSection.tsx`.
- [X] T030 [US3] Implement an `apiService` to communicate with the backend in `frontend/src/services/api.ts`.
- [X] T031 [US3] Manage global state using Zustand in `frontend/src/store/`.
- [X] T032 [US3] Implement loading states and error handling across the UI.

**Checkpoint**: Frontend is functional for the core user flow (without history).

---

## Phase 6: User Story 4 - Histórico e Persistência (Priority: P4)

**Goal**: As a candidate, I want to view my past applications.
**Independent Test**: Generate materials for multiple jobs and verify they appear in the history sidebar and are searchable.

### Implementation for User Story 4

- [X] T033 [US4] Implement a wrapper for IndexedDB in `frontend/src/services/db.ts`.
- [X] T034 [P] [US4] Create the `HistorySidebar` component in `frontend/src/components/HistorySidebar.tsx`.
- [X] T035 [US4] Implement search and filter functionality for the history.
- [X] T036 [US4] Implement history export to JSON.
- [X] T037 [P] [US4] Implement client-side PDF export for CV and cover letter using `jsPDF` in `frontend/src/services/pdf.ts`.

**Checkpoint**: The application is feature-complete on `localhost`.

---

## Phase 7: User Story 5 - Production Deploy (Priority: P5)

**Goal**: As a developer, I want an automated, zero-downtime deployment process.
**Independent Test**: Push a change to the `main` branch and see it deployed automatically to production without service interruption.

### Implementation for User Story 5

- [X] T038 [US5] Create a multi-stage `Dockerfile` for the backend in `backend/Dockerfile`.
- [X] T039 [US5] Configure a CI pipeline in GitHub Actions (`.github/workflows/ci.yml`) to run tests.
- [X] T040 [P] [US5] Setup Vercel for frontend hosting and connect to the GitHub repository.
- [X] T041 [P] [US5] Setup Render/Railway for backend hosting.
- [X] T042 [US5] Configure environment variables for production in Vercel and Render/Railway.
- [X] T043 [US5] Implement `/health` check endpoint in `backend/src/api/endpoints/health.py`.
- [X] T044 [US5] Create deployment documentation in `DEPLOY.md`.

**Checkpoint**: The application is live in production with a CI/CD pipeline.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements that affect multiple user stories.

- [X] T045 [P] Review and update all documentation (`README.md`, `quickstart.md`).
- [X] T046 Code cleanup and refactoring across `frontend/` and `backend/`.
- [X] T047 [P] Add rate limiting to the backend API.
- [X] T048 [P] Add comprehensive security headers and input sanitization.

---

## Dependencies & Execution Order

- **Setup & Foundational (Phases 1-2)** must be completed before any user story work.
- **User Stories (Phases 3-7)** depend on the foundational phase. They can be developed sequentially (P1 -> P2 -> ...) or in parallel.
- **US1 (Extraction)** is a prerequisite for the E2E flow of **US2 (Generation)**.
- **US3 (UI)** depends on the backend APIs from US1 and US2 being available.
- **US4 (History)** depends on US3.
- **US5 (Deploy)** can be worked on in parallel but is only fully testable once features are ready to deploy.

### Parallel Opportunities

- **Backend/Frontend**: Once contracts are defined (T013, T020), frontend development (US3) can start in parallel with backend development (US1, US2) using a mock API.
- **Within Stories**: Tasks marked with `[P]` can be done in parallel. For example, in US1, validation (T016) can be developed alongside the scraper (T015). In US5, Vercel (T040) and Render (T041) setup can happen concurrently.
