"""Logging configuration with structured logging support."""

import logging
import sys

from pythonjsonlogger import jsonlogger

from app.config import get_settings


def setup_logging() -> None:
    """Configure structured logging with JSON format."""
    settings = get_settings()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level.upper())

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level.upper())

    # Create JSON formatter
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
    )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Set log level for specific loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)

    logging.info(
        "Logging configured",
        extra={"log_level": settings.log_level, "environment": settings.app_env},
    )