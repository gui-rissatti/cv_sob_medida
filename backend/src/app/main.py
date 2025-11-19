"""Application entrypoint and FastAPI instance."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from api.routes import register_routes
from core.config import Settings, get_settings
from core.logging import configure_logging
from core.rate_limit import limiter

def create_app() -> FastAPI:
    """Instantiate the FastAPI application with shared metadata."""
    settings = get_settings()
    configure_logging(level=settings.log_level)

    application = FastAPI(
        title="CV Sob Medida API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # State
    application.state.settings = settings
    application.state.limiter = limiter

    # Middleware
    application.add_middleware(SlowAPIMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "*.onrender.com"]
    )

    # Exception Handlers
    application.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    register_routes(application)
    return application


app = create_app()
