"""FastAPI application entry point."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.config import get_settings
from app.database import close_db, engine
from app.logging_config import setup_logging
from app.routes import health, metrics, user_routes
from app.telemetry import (
    instrument_fastapi,
    instrument_sqlalchemy,
    setup_telemetry,
    shutdown_telemetry,
)

# Setup logging first
setup_logging()

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info("Starting application")
    setup_telemetry(settings)
    # Instrument the sync_engine for async SQLAlchemy
    instrument_sqlalchemy(engine.sync_engine)
    logger.info("OpenTelemetry instrumentation initialized")

    yield

    # Shutdown
    logger.info("Shutting down application")
    await close_db()
    shutdown_telemetry()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="OpenTelemetry Python Example API",
    description="A production-ready Python FastAPI REST API with comprehensive OpenTelemetry instrumentation",
    version=__version__,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instrument FastAPI with OpenTelemetry
instrument_fastapi(app)

# Include routers
app.include_router(health.router)
app.include_router(metrics.router)
app.include_router(user_routes.router)

logger.info(
    "Application initialized",
    extra={
        "version": __version__,
        "environment": settings.app_env,
        "service_name": settings.otel_service_name,
    },
)
