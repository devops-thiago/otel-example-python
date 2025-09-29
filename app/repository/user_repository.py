"""User repository for database operations."""

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user_schema import UserCreate, UserUpdate

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for User CRUD operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user.

        Args:
            user_data: User creation data

        Returns:
            Created user object
        """
        user = User(**user_data.model_dump())
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("Created user with id=%d, email=%s", user.id, user.email)
        return user

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None if not found
        """
        result = await self.session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user:
            logger.debug("Found user with id=%d", user_id)
        else:
            logger.debug("User with id=%d not found", user_id)
        return user

    async def get_all(self) -> list[User]:
        """Get all users.

        Returns:
            List of all users
        """
        result = await self.session.execute(select(User))
        users = list(result.scalars().all())
        logger.debug("Retrieved %d users", len(users))
        return users

    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user by ID.

        Args:
            user_id: User ID
            user_data: User update data

        Returns:
            Updated user object or None if not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            logger.warning("Attempted to update non-existent user with id=%d", user_id)
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.session.commit()
        await self.session.refresh(user)
        logger.info("Updated user with id=%d", user_id)
        return user

    async def delete(self, user_id: int) -> bool:
        """Delete user by ID.

        Args:
            user_id: User ID

        Returns:
            True if user was deleted, False if not found
        """
        user = await self.get_by_id(user_id)
        if not user:
            logger.warning("Attempted to delete non-existent user with id=%d", user_id)
            return False

        await self.session.delete(user)
        await self.session.commit()
        logger.info("Deleted user with id=%d", user_id)
        return True

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email.

        Args:
            email: User email

        Returns:
            User object or None if not found
        """
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()