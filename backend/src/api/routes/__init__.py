"""API router registration."""
from __future__ import annotations

from fastapi import APIRouter, FastAPI

from . import extraction, generation, health

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(extraction.router)
router.include_router(generation.router)


def register_routes(app: FastAPI) -> None:
    """Attach all routers to the FastAPI application."""
    app.include_router(router)
