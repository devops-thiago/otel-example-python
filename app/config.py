"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database Configuration
    db_host: str = Field(default="localhost", description="Database host")
    db_port: int = Field(default=3306, description="Database port")
    db_user: str = Field(default="root", description="Database user")
    db_password: str = Field(default="password", description="Database password")
    db_name: str = Field(default="otel_example", description="Database name")

    # Server Configuration
    server_host: str = Field(default="0.0.0.0", description="Server host")
    server_port: int = Field(default=8080, description="Server port")
    app_env: str = Field(default="development", description="Application environment")
    log_level: str = Field(default="info", description="Logging level")

    # OpenTelemetry Configuration
    otel_service_name: str = Field(
        default="otel-example-python", description="OpenTelemetry service name"
    )
    otel_service_version: str = Field(
        default="1.0.0", description="OpenTelemetry service version"
    )
    otel_environment: str = Field(
        default="development", description="OpenTelemetry environment"
    )
    otel_exporter_otlp_endpoint: str = Field(
        default="localhost:4320", description="OTLP exporter endpoint"
    )
    otel_enable_tracing: bool = Field(
        default=True, description="Enable OpenTelemetry tracing"
    )
    otel_enable_metrics: bool = Field(
        default=True, description="Enable OpenTelemetry metrics"
    )
    otel_enable_logging: bool = Field(
        default=True, description="Enable OpenTelemetry logging"
    )

    @property
    def database_url(self) -> str:
        """Get the database URL for SQLAlchemy."""
        return (
            f"mysql+aiomysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    @property
    def database_url_sync(self) -> str:
        """Get the synchronous database URL for SQLAlchemy."""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
