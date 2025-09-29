"""User API routes."""

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreate,
    UserListResponse,
    UserResponse,
    UserUpdate,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user with the provided information",
)
async def create_user(
    user_data: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """Create a new user."""
    repository = UserRepository(db)

    # Check if email already exists
    existing_user = await repository.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {user_data.email} already exists",
        )

    user = await repository.create(user_data)
    return UserResponse.model_validate(user)


@router.get(
    "",
    response_model=UserListResponse,
    summary="Get all users",
    description="Retrieve a list of all users",
)
async def get_users(db: Annotated[AsyncSession, Depends(get_db)]) -> UserListResponse:
    """Get all users."""
    repository = UserRepository(db)
    users = await repository.get_all()
    return UserListResponse(
        users=[UserResponse.model_validate(user) for user in users],
        total=len(users),
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their ID",
)
async def get_user(
    user_id: int, db: Annotated[AsyncSession, Depends(get_db)]
) -> UserResponse:
    """Get user by ID."""
    repository = UserRepository(db)
    user = await repository.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return UserResponse.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user's information",
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UserResponse:
    """Update user by ID."""
    repository = UserRepository(db)

    # Check if email is being updated and if it already exists
    if user_data.email:
        existing_user = await repository.get_by_email(user_data.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email {user_data.email} already exists",
            )

    user = await repository.update(user_id, user_data)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    return UserResponse.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by their ID",
)
async def delete_user(
    user_id: int, db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    """Delete user by ID."""
    repository = UserRepository(db)
    deleted = await repository.delete(user_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
