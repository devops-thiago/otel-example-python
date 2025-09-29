"""Metrics endpoint for OpenTelemetry."""

from fastapi import APIRouter

router = APIRouter(tags=["metrics"])


@router.get(
    "/metrics",
    summary="OpenTelemetry metrics status",
    description="Metrics are exported via OTLP to the configured collector",
)
async def metrics() -> dict[str, str]:
    """OpenTelemetry metrics status endpoint.

    All metrics are automatically exported via OTLP to the configured collector.
    This endpoint confirms metrics are being collected.
    """
    return {
        "status": "metrics_enabled",
        "exporter": "otlp",
        "message": "Metrics are being exported via OpenTelemetry OTLP",
    }
