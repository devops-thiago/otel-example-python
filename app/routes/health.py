"""Health check endpoints."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description="Basic health check endpoint",
    status_code=status.HTTP_200_OK,
)
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@router.get(
    "/ready",
    summary="Readiness check",
    description="Readiness check including database connectivity",
    status_code=status.HTTP_200_OK,
)
async def ready(db: Annotated[AsyncSession, Depends(get_db)]) -> JSONResponse:
    """Readiness check endpoint with database verification."""
    try:
        # Check database connection
        await db.execute(text("SELECT 1"))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "ready", "database": "connected"},
        )
    except Exception as e:
        logger.error("Readiness check failed: %s", str(e))
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "database": "disconnected", "error": str(e)},
        )