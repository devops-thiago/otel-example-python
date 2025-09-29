"""OpenTelemetry instrumentation setup."""

import logging

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.config import Settings

logger = logging.getLogger(__name__)


def setup_telemetry(settings: Settings) -> None:
    """Initialize OpenTelemetry instrumentation.

    Args:
        settings: Application settings
    """
    # Create resource with service information
    resource = Resource.create(
        {
            "service.name": settings.otel_service_name,
            "service.version": settings.otel_service_version,
            "deployment.environment": settings.otel_environment,
        }
    )

    # Setup tracing if enabled
    if settings.otel_enable_tracing:
        trace_provider = TracerProvider(resource=resource)
        span_exporter = OTLPSpanExporter(
            endpoint=settings.otel_exporter_otlp_endpoint, insecure=True
        )
        trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        trace.set_tracer_provider(trace_provider)
        logger.info(
            "OpenTelemetry tracing initialized with endpoint: %s",
            settings.otel_exporter_otlp_endpoint,
        )

    # Setup metrics if enabled
    if settings.otel_enable_metrics:
        metric_exporter = OTLPMetricExporter(
            endpoint=settings.otel_exporter_otlp_endpoint, insecure=True
        )
        metric_reader = PeriodicExportingMetricReader(
            metric_exporter, export_interval_millis=60000
        )
        meter_provider = MeterProvider(
            resource=resource, metric_readers=[metric_reader]
        )
        metrics.set_meter_provider(meter_provider)

        # Instrument system metrics (CPU, memory, network, disk)
        # Use default configuration by not passing config parameter
        SystemMetricsInstrumentor().instrument()

        logger.info("OpenTelemetry metrics initialized with system instrumentation")

    # Setup logging instrumentation if enabled
    if settings.otel_enable_logging:
        # Create OTLP log exporter
        log_exporter = OTLPLogExporter(
            endpoint=settings.otel_exporter_otlp_endpoint, insecure=True
        )

        # Create logger provider with batch processor
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        set_logger_provider(logger_provider)

        # Attach OTLP handler to root logger
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        logging.getLogger().addHandler(handler)

        logger.info("OpenTelemetry logging initialized with OTLP exporter")


def instrument_fastapi(app: object) -> None:
    """Instrument FastAPI application.

    Args:
        app: FastAPI application instance
    """
    FastAPIInstrumentor.instrument_app(app)  # type: ignore[arg-type]
    logger.info("FastAPI instrumented with OpenTelemetry")


def instrument_sqlalchemy(engine: object) -> None:
    """Instrument SQLAlchemy engine.

    Args:
        engine: SQLAlchemy engine instance
    """
    SQLAlchemyInstrumentor().instrument(engine=engine)
    logger.info("SQLAlchemy instrumented with OpenTelemetry")


def shutdown_telemetry() -> None:
    """Shutdown OpenTelemetry providers."""
    from opentelemetry._logs import get_logger_provider

    trace_provider = trace.get_tracer_provider()
    if hasattr(trace_provider, "shutdown"):
        trace_provider.shutdown()
        logger.info("OpenTelemetry tracer provider shut down")

    meter_provider = metrics.get_meter_provider()
    if hasattr(meter_provider, "shutdown"):
        meter_provider.shutdown()
        logger.info("OpenTelemetry meter provider shut down")

    logger_provider = get_logger_provider()
    if hasattr(logger_provider, "shutdown"):
        logger_provider.shutdown()
        logger.info("OpenTelemetry logger provider shut down")
