"""Unit tests for user API routes."""

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.models import User

client = TestClient(app)


@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    return User(
        id=1,
        name="John Doe",
        email="john@example.com",
        bio="Software Engineer",
        created_at=datetime(2025, 1, 1),
        updated_at=datetime(2025, 1, 1),
    )


class TestCreateUser:
    """Tests for POST /api/users endpoint."""

    @patch("app.routes.user_routes.UserRepository")
    def test_create_user_success(self, mock_repo_class: AsyncMock, sample_user: User) -> None:
        """Test successful user creation."""
        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = None
        mock_repo.create.return_value = sample_user
        mock_repo_class.return_value = mock_repo

        response = client.post(
            "/api/users",
            json={
                "name": "John Doe",
                "email": "john@example.com",
                "bio": "Software Engineer",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["id"] == 1

    @patch("app.routes.user_routes.UserRepository")
    def test_create_user_duplicate_email(
        self, mock_repo_class: AsyncMock, sample_user: User
    ) -> None:
        """Test creating user with duplicate email."""
        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = sample_user
        mock_repo_class.return_value = mock_repo

        response = client.post(
            "/api/users",
            json={
                "name": "Jane Doe",
                "email": "john@example.com",
                "bio": "Engineer",
            },
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    def test_create_user_invalid_email(self) -> None:
        """Test creating user with invalid email."""
        response = client.post(
            "/api/users",
            json={"name": "John Doe", "email": "invalid-email", "bio": "Engineer"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_user_missing_name(self) -> None:
        """Test creating user without name."""
        response = client.post(
            "/api/users",
            json={"email": "john@example.com", "bio": "Engineer"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetUsers:
    """Tests for GET /api/users endpoint."""

    @patch("app.routes.user_routes.UserRepository")
    def test_get_all_users_success(self, mock_repo_class: AsyncMock) -> None:
        """Test getting all users."""
        users = [
            User(
                id=1,
                name="John",
                email="john@example.com",
                bio="Dev",
                created_at=datetime(2025, 1, 1),
                updated_at=datetime(2025, 1, 1),
            ),
            User(
                id=2,
                name="Jane",
                email="jane@example.com",
                bio="Engineer",
                created_at=datetime(2025, 1, 1),
                updated_at=datetime(2025, 1, 1),
            ),
        ]

        mock_repo = AsyncMock()
        mock_repo.get_all.return_value = users
        mock_repo_class.return_value = mock_repo

        response = client.get("/api/users")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        assert len(data["users"]) == 2
        assert data["users"][0]["name"] == "John"
        assert data["users"][1]["name"] == "Jane"

    @patch("app.routes.user_routes.UserRepository")
    def test_get_all_users_empty(self, mock_repo_class: AsyncMock) -> None:
        """Test getting users when none exist."""
        mock_repo = AsyncMock()
        mock_repo.get_all.return_value = []
        mock_repo_class.return_value = mock_repo

        response = client.get("/api/users")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 0
        assert len(data["users"]) == 0


class TestGetUserById:
    """Tests for GET /api/users/{id} endpoint."""

    @patch("app.routes.user_routes.UserRepository")
    def test_get_user_by_id_success(
        self, mock_repo_class: AsyncMock, sample_user: User
    ) -> None:
        """Test getting user by ID."""
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = sample_user
        mock_repo_class.return_value = mock_repo

        response = client.get("/api/users/1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"

    @patch("app.routes.user_routes.UserRepository")
    def test_get_user_by_id_not_found(self, mock_repo_class: AsyncMock) -> None:
        """Test getting non-existent user."""
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        mock_repo_class.return_value = mock_repo

        response = client.get("/api/users/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]


class TestUpdateUser:
    """Tests for PUT /api/users/{id} endpoint."""

    @patch("app.routes.user_routes.UserRepository")
    def test_update_user_success(
        self, mock_repo_class: AsyncMock, sample_user: User
    ) -> None:
        """Test successful user update."""
        updated_user = User(
            id=1,
            name="John Updated",
            email="john@example.com",
            bio="Senior Engineer",
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 2),
        )

        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = None
        mock_repo.update.return_value = updated_user
        mock_repo_class.return_value = mock_repo

        response = client.put(
            "/api/users/1",
            json={"name": "John Updated", "bio": "Senior Engineer"},
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "John Updated"
        assert data["bio"] == "Senior Engineer"

    @patch("app.routes.user_routes.UserRepository")
    def test_update_user_not_found(self, mock_repo_class: AsyncMock) -> None:
        """Test updating non-existent user."""
        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = None
        mock_repo.update.return_value = None
        mock_repo_class.return_value = mock_repo

        response = client.put(
            "/api/users/999",
            json={"name": "John Updated"},
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch("app.routes.user_routes.UserRepository")
    def test_update_user_duplicate_email(
        self, mock_repo_class: AsyncMock, sample_user: User
    ) -> None:
        """Test updating user with email that belongs to another user."""
        other_user = User(
            id=2,
            name="Other User",
            email="other@example.com",
            bio="Other",
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 1),
        )

        mock_repo = AsyncMock()
        mock_repo.get_by_email.return_value = other_user
        mock_repo_class.return_value = mock_repo

        response = client.put(
            "/api/users/1",
            json={"email": "other@example.com"},
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]


class TestDeleteUser:
    """Tests for DELETE /api/users/{id} endpoint."""

    @patch("app.routes.user_routes.UserRepository")
    def test_delete_user_success(self, mock_repo_class: AsyncMock) -> None:
        """Test successful user deletion."""
        mock_repo = AsyncMock()
        mock_repo.delete.return_value = True
        mock_repo_class.return_value = mock_repo

        response = client.delete("/api/users/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @patch("app.routes.user_routes.UserRepository")
    def test_delete_user_not_found(self, mock_repo_class: AsyncMock) -> None:
        """Test deleting non-existent user."""
        mock_repo = AsyncMock()
        mock_repo.delete.return_value = False
        mock_repo_class.return_value = mock_repo

        response = client.delete("/api/users/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self) -> None:
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "healthy"