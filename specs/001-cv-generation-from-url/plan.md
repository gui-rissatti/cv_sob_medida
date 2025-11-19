# Implementation Plan: CV Generation from URL

## 1. Technical Context

| Category      | Decision                               | Justification                                                                 |
|---------------|----------------------------------------|-------------------------------------------------------------------------------|
| **Backend**   | FastAPI 0.104+                         | ASGI support for asynchronous operations, modern, high-performance.           |
|               | LangChain 0.1+ & LangSmith             | Consolidated framework for LLM orchestration, observability with LangSmith.   |
|               | Google Gemini 1.5 Pro                  | Advanced LLM for content extraction and generation.                           |
|               | BeautifulSoup4 + httpx                 | Robust and standard libraries for web scraping and HTTP requests.             |
|               | Structlog                              | Structured logging for better observability.                                  |
|               | Tenacity                               | Simple and powerful retry logic implementation.                               |
| **Frontend**  | React 19.2 + TypeScript 5.8            | Industry standard for building interactive UIs with strong type safety.       |
|               | Vite 6.2                               | Fast build tool and development server.                                       |
|               | Tailwind CSS                           | Utility-first CSS framework for rapid UI development.                         |
|               | jsPDF + pdf-lib                        | Client-side PDF generation, reducing server load.                             |
|               | IndexedDB                              | Local storage for user's application history.                                 |
| **DevOps**    | Docker                                 | Containerization for consistent development and production environments.      |
|               | GitHub Actions                         | CI/CD automation integrated with the source repository.                       |
|               | Vercel                                 | Optimized hosting for frontend applications.                                  |
|               | Render/Railway                         | Managed hosting for backend services.                                         |
| **Unknowns**  | Prioritized Job Boards                 | LinkedIn, Gupy, Indeed (see `research.md`)                            |
|               | PDF Generation Location                | Client-side (jsPDF) chosen to reduce server load.                             |
|               | User Rate Limiting                     | 10 req/min per IP (see `research.md`)                                         |

## 2. Constitution Check

The `constitution.md` file is a template and has not been configured for this project. The plan will proceed based on the gates defined in the feature specification.

| Gate                   | Status      | Notes                                                                |
|------------------------|-------------|----------------------------------------------------------------------|
| **Simplicity Gate**    | PASS        | Project structure will be limited to backend, frontend, shared-types.  |
| **Anti-Abstraction**   | PASS        | LangChain will be used directly without unnecessary wrappers.        |
| **Integration-First**  | PENDING     | API contracts need to be defined and tested before implementation.   |


## 4. Phase 0: Outline & Research (Completed)

*   **Task 1:** Research and decide on the priority list of job boards to support for scraping (e.g., LinkedIn, Gupy, Indeed). - **DONE**
*   **Task 2:** Define the rate-limiting strategy for users (e.g., per IP, per user account if authentication is added). - **DONE**
*   **Task 3:** Create `research.md` to document decisions. - **DONE**

## 5. Phase 1: Design & Contracts

*   **Task 1:** Create `data-model.md` to define the data structures for Job, CV, and Application History.
*   **Task 2:** Generate OpenAPI 3.0 specification for the backend API in `/contracts/openapi.yml`.
*   **Task 3:** Create a `quickstart.md` guide for setting up the development environment.
*   **Task 4:** Update agent context with the new technologies.

I will now proceed with reading the constitution file and creating the `research.md` file.
