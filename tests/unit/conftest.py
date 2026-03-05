"""Unit test configuration and shared fixtures."""

from collections.abc import AsyncGenerator, Generator
from unittest.mock import MagicMock

import pytest

from app.database import get_db
from app.main import app


@pytest.fixture(autouse=True)
def override_get_db() -> Generator[None, None, None]:
    """Override the get_db dependency to prevent real DB connections in unit tests."""
    mock_session = MagicMock()

    async def mock_get_db() -> AsyncGenerator[MagicMock, None]:
        yield mock_session

    app.dependency_overrides[get_db] = mock_get_db
    yield
    app.dependency_overrides.clear()
