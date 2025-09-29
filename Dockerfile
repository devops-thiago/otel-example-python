FROM python:3.12-slim AS deps

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root

FROM python:3.12-slim AS builder

ARG VERSION=dev
ARG BUILD_DATE
ARG VCS_REF

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3

COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

COPY pyproject.toml ./
COPY app/ ./app/

RUN find . -name '*_test.py' -type f -delete && \
    find . -name 'test_*.py' -type f -delete && \
    find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

FROM python:3.12-slim

ARG VERSION=dev
ARG BUILD_DATE
ARG VCS_REF

LABEL org.opencontainers.image.title="OpenTelemetry Python CRUD API" \
      org.opencontainers.image.description="Python FastAPI REST API with OpenTelemetry instrumentation" \
      org.opencontainers.image.authors="support@arquivolivre.com.br" \
      org.opencontainers.image.vendor="Arquivo Livre" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/devops-thiago/otel-example-python" \
      org.opencontainers.image.documentation="https://github.com/devops-thiago/otel-example-python/blob/main/README.md" \
      org.opencontainers.image.licenses="MIT"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        && rm -rf /var/lib/apt/lists/* && \
    groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/bash -m appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

WORKDIR /app

COPY --from=builder --chown=root:root /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder --chown=root:root /usr/local/bin /usr/local/bin
COPY --from=builder --chown=appuser:appuser /app/app ./app

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]