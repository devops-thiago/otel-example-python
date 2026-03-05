# OpenTelemetry Python Example

[![CI](https://img.shields.io/github/actions/workflow/status/devops-thiago/otel-example-python/ci.yml?branch=main&label=CI)](https://github.com/devops-thiago/otel-example-python/actions)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue?logo=python)](https://www.python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.131%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/github/license/devops-thiago/otel-example-python)](LICENSE)
[![Codecov](https://img.shields.io/codecov/c/github/devops-thiago/otel-example-python?label=coverage)](https://app.codecov.io/gh/devops-thiago/otel-example-python)
[![Sonar Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=devops-thiago_otel-example-python&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=devops-thiago_otel-example-python)
[![Sonar Coverage](https://sonarcloud.io/api/project_badges/measure?project=devops-thiago_otel-example-python&metric=coverage)](https://sonarcloud.io/summary/new_code?id=devops-thiago_otel-example-python)
[![OpenTelemetry](https://img.shields.io/badge/OpenTelemetry-enabled-blue?logo=opentelemetry)](https://opentelemetry.io)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker)](https://www.docker.com)
[![Docker Hub](https://img.shields.io/docker/v/thiagosg/otel-crud-api-python?logo=docker&label=Docker%20Hub)](https://hub.docker.com/r/thiagosg/otel-crud-api-python)
[![Docker Pulls](https://img.shields.io/docker/pulls/thiagosg/otel-crud-api-python)](https://hub.docker.com/r/thiagosg/otel-crud-api-python)

A production-ready Python FastAPI REST API with comprehensive OpenTelemetry instrumentation, featuring distributed tracing, metrics collection, and structured logging. Built with clean architecture principles and designed for cloud-native deployments.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Docker](#docker)
- [Observability](#observability)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **🚀 FastAPI** - Modern async Python web framework with automatic OpenAPI documentation
- **📊 Full Observability** - Distributed tracing, metrics, and structured logging
- **🔌 OpenTelemetry Native** - Built-in OTLP exporter support
- **🏗️ Clean Architecture** - Repository pattern with separation of concerns
- **🐳 Docker Ready** - Multi-stage Dockerfile with security best practices
- **🔒 Security First** - Non-root user, minimal attack surface
- **🧪 Well Tested** - Comprehensive test coverage with pytest
- **📝 Type Safety** - Full type hints with mypy strict mode
- **💅 Code Quality** - Black formatting, Ruff linting, PEP8 compliance
- **💾 MySQL Integration** - Async SQLAlchemy with proper instrumentation

## 📚 Prerequisites

- Python 3.11+ (for local development)
- Poetry (Python dependency management)
- Docker & Docker Compose
- MySQL 8.0+ (or use the provided docker-compose)
- OpenTelemetry Collector (optional - included in full setup)

## 🚀 Quick Start

### Option 1: Full Stack (App + Database + Observability)

```bash
# Clone the repository
git clone https://github.com/devops-thiago/otel-example-python.git
cd otel-example-python

# Start everything with docker-compose
docker-compose up -d

# Check if services are running
docker-compose ps
```

**Access points:**
- API: http://localhost:8080
- API Docs (Swagger): http://localhost:8080/docs
- Health: http://localhost:8080/health
- Metrics: http://localhost:8080/metrics
- Grafana: http://localhost:3000 (admin/admin)

### Option 2: Run Locally

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
make install
# or: poetry install

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## 📖 API Documentation

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check endpoint |
| GET | `/ready` | Readiness check endpoint |
| GET | `/metrics` | OpenTelemetry metrics status |

### User API

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/api/users` | List all users | - |
| GET | `/api/users/{id}` | Get user by ID | - |
| POST | `/api/users` | Create new user | `{"name": "John", "email": "john@example.com", "bio": "Developer"}` |
| PUT | `/api/users/{id}` | Update user | `{"name": "John Updated"}` |
| DELETE | `/api/users/{id}` | Delete user | - |

### Example Requests

```bash
# Create a user
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "bio": "Software Engineer"}'

# Get all users
curl http://localhost:8080/api/users

# Get user by ID
curl http://localhost:8080/api/users/1

# Update user
curl -X PUT http://localhost:8080/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "John Updated"}'

# Delete user
curl -X DELETE http://localhost:8080/api/users/1
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| **OpenTelemetry** | | |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OTLP collector endpoint | `localhost:4320` |
| `OTEL_SERVICE_NAME` | Service name for telemetry | `otel-example-python` |
| `OTEL_ENABLE_TRACING` | Enable distributed tracing | `true` |
| `OTEL_ENABLE_METRICS` | Enable metrics collection | `true` |
| `OTEL_ENABLE_LOGGING` | Enable OTLP log export | `true` |
| **Database** | | |
| `DB_HOST` | MySQL host | `localhost` |
| `DB_PORT` | MySQL port | `3306` |
| `DB_USER` | MySQL user | `appuser` |
| `DB_PASSWORD` | MySQL password | `apppassword` |
| `DB_NAME` | MySQL database name | `otel_example` |
| **Server** | | |
| `SERVER_HOST` | API server host | `0.0.0.0` |
| `SERVER_PORT` | API server port | `8080` |
| `APP_ENV` | Application environment | `development` |
| `LOG_LEVEL` | Log level (debug/info/warn/error) | `info` |

## 🏗️ Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── telemetry.py         # OpenTelemetry setup
│   ├── logging_config.py    # Structured logging
│   ├── middleware/          # HTTP middleware
│   ├── repository/          # Data access layer
│   │   └── user_repository.py
│   ├── routes/              # API routes
│   │   ├── health.py
│   │   ├── metrics.py
│   │   └── user_routes.py
│   └── schemas/             # Pydantic schemas
│       └── user_schema.py
├── config/                  # Observability stack configs
│   ├── alloy.alloy          # Grafana Alloy configuration
│   ├── tempo.yaml           # Tempo tracing backend
│   ├── mimir.yaml           # Mimir metrics backend
│   ├── loki.yaml            # Loki logging backend
│   └── grafana/             # Grafana provisioning
├── tests/
│   ├── unit/                # Unit tests
│   └── integration/         # Integration tests
├── docker-compose.yml       # Full stack deployment
├── docker-compose.app-only.yml  # App-only deployment
├── Dockerfile               # Multi-stage Docker build
├── pyproject.toml           # Poetry dependencies & config
├── Makefile                 # Development commands
└── README.md                # This file
```

## 🛠️ Development

### Local Development Setup

```bash
# Clone and setup
git clone https://github.com/devops-thiago/otel-example-python.git
cd otel-example-python

# Install dependencies
make install

# Run linting
make lint

# Format code
make format

# Type check
make type-check

# Run tests
make test

# Run tests with coverage
make coverage
```

### Available Make Commands

```bash
make install         # Install dependencies with Poetry
make test            # Run tests
make coverage        # Run tests with coverage report
make lint            # Run ruff linter
make format          # Format code with black
make format-check    # Check code formatting
make type-check      # Run mypy type checking
make docker-build    # Build Docker image
make docker-up       # Start all services
make docker-down     # Stop all services
make clean           # Clean build artifacts
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run tests with coverage
make coverage

# Run specific test file
poetry run pytest tests/unit/test_user_repository.py -v

# Run with verbose output
poetry run pytest tests/ -vv
```

## 🔍 Observability

This application exports telemetry data in OTLP format:

- **Traces**: Distributed tracing for all HTTP requests and database operations
- **Metrics**: Request duration, database connection pool, custom business metrics
- **Logs**: Structured JSON logs with trace correlation

### Viewing Telemetry Data

#### Grafana (included in docker-compose)

```bash
# Access Grafana
open http://localhost:3000
# Default credentials: admin/admin
```

Grafana comes pre-configured with datasources for:
- Tempo (traces)
- Mimir (metrics)
- Loki (logs)

## 🐳 Docker Deployment

### Building Docker Image

```bash
# Build locally
make docker-build

# Build with version information
docker build \
  --build-arg VERSION=1.0.0 \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  -t otel-example-python:latest .
```

### Using Pre-built Docker Image

```bash
# Pull from Docker Hub
docker pull thiagosg/otel-example-python:latest

# Run with custom environment
docker run -d \
  -p 8080:8080 \
  -e OTEL_EXPORTER_OTLP_ENDPOINT=your-collector:4317 \
  -e DB_HOST=your-db-host \
  thiagosg/otel-example-python:latest
```

## 🤝 Contributing

### Code Quality Standards

All contributions must pass:
- ✅ Linting (ruff)
- ✅ Formatting (black)
- ✅ Type checking (mypy)
- ✅ Tests with coverage
- ✅ PEP8 compliance

### Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters (`make test && make lint && make type-check`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Automated Dependency Updates

This repository uses **Dependabot** to automatically keep dependencies up to date:
- 🔄 **Weekly updates** every Monday at 09:00 UTC
- 📦 **Python packages** (via Poetry/pyproject.toml)
- 🐳 **Docker images** (base images and tools)
- ⚙️ **GitHub Actions** (workflow dependencies)
- 🏷️ **Grouped updates** for related packages (OpenTelemetry, FastAPI, dev tools)

## 📦 Technology Stack

- **Framework**: FastAPI 0.115+
- **Database**: MySQL 8.0 with async SQLAlchemy
- **Observability**: OpenTelemetry (OTLP)
- **Validation**: Pydantic V2
- **Testing**: pytest with pytest-asyncio
- **Code Quality**: Black, Ruff, Mypy
- **Dependency Management**: Poetry + Dependabot
- **Containerization**: Docker with multi-stage builds

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

