.PHONY: install test coverage lint format format-check type-check docker-build docker-up docker-down clean help

help:
	@echo "Available commands:"
	@echo "  install         - Install dependencies with Poetry"
	@echo "  test            - Run tests"
	@echo "  coverage        - Run tests with coverage report"
	@echo "  lint            - Run ruff linter"
	@echo "  format          - Format code with black"
	@echo "  format-check    - Check code formatting"
	@echo "  type-check      - Run mypy type checking"
	@echo "  docker-build    - Build Docker image"
	@echo "  docker-up       - Start all services with docker-compose"
	@echo "  docker-down     - Stop all services"
	@echo "  clean           - Clean build artifacts and caches"

install:
	@echo "Installing dependencies..."
	poetry install

test:
	@echo "Running tests..."
	poetry run pytest tests/ -v

coverage:
	@echo "Running tests with coverage..."
	poetry run pytest tests/ --cov=app --cov-report=term-missing --cov-report=html --cov-report=xml

lint:
	@echo "Running ruff linter..."
	poetry run ruff check app/ tests/

format:
	@echo "Formatting code with black..."
	poetry run black app/ tests/
	@echo "Sorting imports with ruff..."
	poetry run ruff check --select I --fix app/ tests/

format-check:
	@echo "Checking code formatting..."
	poetry run black --check app/ tests/
	poetry run ruff check app/ tests/

type-check:
	@echo "Running mypy type checking..."
	poetry run mypy app/

docker-build:
	@echo "Building Docker image..."
	docker build -t otel-example-python:latest .

docker-up:
	@echo "Starting services with docker-compose..."
	docker-compose up -d

docker-down:
	@echo "Stopping services..."
	docker-compose down

clean:
	@echo "Cleaning build artifacts and caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "coverage.xml" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "Clean complete"