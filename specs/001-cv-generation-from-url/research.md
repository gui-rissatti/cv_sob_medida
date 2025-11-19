# Research & Decisions

This document records the research and decisions made to resolve the "NEEDS CLARIFICATION" items from the implementation plan.

## 1. Prioritized Job Boards for Scraping

*   **Decision**: The following job boards will be prioritized for scraping support:
    1.  LinkedIn
    2.  Gupy
    3.  Indeed
*   **Rationale**: These platforms cover a significant portion of the job market in the target region and represent a good mix of technical challenges for the scraper.
*   **Alternatives Considered**: Catho, Vagas.com.br. These can be added in a future iteration.

## 2. User Rate Limiting

*   **Decision**: A rate limit of 10 requests per minute per IP address will be implemented.
*   **Rationale**: This provides a baseline level of protection against abuse while allowing for legitimate, intensive use of the application. As the user base grows and authentication is potentially introduced, this can be revisited to implement more sophisticated user-based limits.
*   **Alternatives Considered**: No rate limiting (high risk of abuse), stricter limits (could hinder user experience).
