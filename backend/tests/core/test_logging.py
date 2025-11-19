"""Tests for structlog configuration."""
from __future__ import annotations

import logging

from structlog.testing import capture_logs


def test_configure_logging_returns_logger() -> None:
    from core.logging import configure_logging

    logger = configure_logging(level="INFO")

    assert hasattr(logger, "info")
    # Logger should emit JSON-like strings when logging
    with capture_logs() as captured:
        logger.info("hello", key="value")

    assert captured[0]["event"] == "hello"
    assert captured[0]["key"] == "value"
