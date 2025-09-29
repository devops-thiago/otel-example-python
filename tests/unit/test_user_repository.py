"""Unit tests for UserRepository."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


@pytest.fixture
def mock_session() -> AsyncMock:
    """Create a mock async session."""
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def repository(mock_session: AsyncMock) -> UserRepository:
    """Create a UserRepository instance with mock session."""
    return UserRepository(mock_session)


@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    user = User(
        id=1,
        name="John Doe",
        email="john@example.com",
        bio="Software Engineer",
        created_at=datetime(2025, 1, 1, 0, 0, 0),
        updated_at=datetime(2025, 1, 1, 0, 0, 0),
    )
    return user


@pytest.mark.asyncio
class TestUserRepositoryCreate:
    """Tests for create method."""

    async def test_create_user_success(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test successful user creation."""
        user_data = UserCreate(
            name="John Doe", email="john@example.com", bio="Software Engineer"
        )

        # Mock the created user
        created_user = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            bio="Software Engineer",
            created_at=datetime(2025, 1, 1),
            updated_at=datetime(2025, 1, 1),
        )

        mock_session.refresh = AsyncMock()
        mock_session.refresh.side_effect = lambda user: setattr(user, "id", 1)

        result = await repository.create(user_data)

        assert result.name == "John Doe"
        assert result.email == "john@example.com"
        assert result.bio == "Software Engineer"
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
class TestUserRepositoryGetById:
    """Tests for get_by_id method."""

    async def test_get_by_id_found(
        self,
        repository: UserRepository,
        mock_session: AsyncMock,
        sample_user: User,
    ) -> None:
        """Test getting user by ID when user exists."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_id(1)

        assert result is not None
        assert result.id == 1
        assert result.name == "John Doe"
        assert result.email == "john@example.com"
        mock_session.execute.assert_called_once()

    async def test_get_by_id_not_found(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test getting user by ID when user does not exist."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_id(999)

        assert result is None
        mock_session.execute.assert_called_once()


@pytest.mark.asyncio
class TestUserRepositoryGetAll:
    """Tests for get_all method."""

    async def test_get_all_with_users(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test getting all users when users exist."""
        users = [
            User(id=1, name="John", email="john@example.com", bio="Dev"),
            User(id=2, name="Jane", email="jane@example.com", bio="Engineer"),
        ]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = users
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        result = await repository.get_all()

        assert len(result) == 2
        assert result[0].name == "John"
        assert result[1].name == "Jane"
        mock_session.execute.assert_called_once()

    async def test_get_all_empty(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test getting all users when no users exist."""
        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        mock_session.execute.return_value = mock_result

        result = await repository.get_all()

        assert len(result) == 0
        mock_session.execute.assert_called_once()


@pytest.mark.asyncio
class TestUserRepositoryUpdate:
    """Tests for update method."""

    async def test_update_user_success(
        self,
        repository: UserRepository,
        mock_session: AsyncMock,
        sample_user: User,
    ) -> None:
        """Test successful user update."""
        update_data = UserUpdate(name="John Updated", bio="Senior Engineer")

        # Mock get_by_id
        with patch.object(repository, "get_by_id", return_value=sample_user):
            result = await repository.update(1, update_data)

            assert result is not None
            assert result.name == "John Updated"
            assert result.bio == "Senior Engineer"
            mock_session.commit.assert_called_once()
            mock_session.refresh.assert_called_once()

    async def test_update_user_not_found(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test updating user that does not exist."""
        update_data = UserUpdate(name="John Updated")

        with patch.object(repository, "get_by_id", return_value=None):
            result = await repository.update(999, update_data)

            assert result is None
            mock_session.commit.assert_not_called()

    async def test_update_user_partial(
        self,
        repository: UserRepository,
        mock_session: AsyncMock,
        sample_user: User,
    ) -> None:
        """Test partial user update."""
        update_data = UserUpdate(bio="New bio only")

        with patch.object(repository, "get_by_id", return_value=sample_user):
            result = await repository.update(1, update_data)

            assert result is not None
            assert result.name == "John Doe"  # Unchanged
            assert result.bio == "New bio only"  # Changed
            mock_session.commit.assert_called_once()


@pytest.mark.asyncio
class TestUserRepositoryDelete:
    """Tests for delete method."""

    async def test_delete_user_success(
        self,
        repository: UserRepository,
        mock_session: AsyncMock,
        sample_user: User,
    ) -> None:
        """Test successful user deletion."""
        with patch.object(repository, "get_by_id", return_value=sample_user):
            result = await repository.delete(1)

            assert result is True
            mock_session.delete.assert_called_once_with(sample_user)
            mock_session.commit.assert_called_once()

    async def test_delete_user_not_found(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test deleting user that does not exist."""
        with patch.object(repository, "get_by_id", return_value=None):
            result = await repository.delete(999)

            assert result is False
            mock_session.delete.assert_not_called()
            mock_session.commit.assert_not_called()


@pytest.mark.asyncio
class TestUserRepositoryGetByEmail:
    """Tests for get_by_email method."""

    async def test_get_by_email_found(
        self,
        repository: UserRepository,
        mock_session: AsyncMock,
        sample_user: User,
    ) -> None:
        """Test getting user by email when user exists."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_email("john@example.com")

        assert result is not None
        assert result.email == "john@example.com"
        mock_session.execute.assert_called_once()

    async def test_get_by_email_not_found(
        self, repository: UserRepository, mock_session: AsyncMock
    ) -> None:
        """Test getting user by email when user does not exist."""
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        result = await repository.get_by_email("nonexistent@example.com")

        assert result is None
        mock_session.execute.assert_called_once()