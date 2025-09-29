"""Pydantic schemas for User API."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    bio: str | None = Field(None, description="User's biography")


class UserCreate(UserBase):
    """Schema for creating a user."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "bio": "Software Engineer",
            }
        }
    )


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    name: str | None = Field(
        None, min_length=1, max_length=100, description="User's full name"
    )
    email: EmailStr | None = Field(None, description="User's email address")
    bio: str | None = Field(None, description="User's biography")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John Updated",
                "bio": "Senior Software Engineer",
            }
        }
    )


class UserResponse(UserBase):
    """Schema for user response."""

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    """Schema for list of users response."""

    users: list[UserResponse] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "users": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john@example.com",
                        "bio": "Software Engineer",
                        "created_at": "2025-01-01T00:00:00",
                        "updated_at": "2025-01-01T00:00:00",
                    }
                ],
                "total": 1,
            }
        }
    )
