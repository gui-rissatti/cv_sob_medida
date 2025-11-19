"""Health check endpoint."""
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Health check", tags=["health"])
def health_check() -> dict[str, str]:
    """Return basic service availability info."""
    return {"status": "ok"}
