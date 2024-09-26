from datetime import datetime

from pydantic import BaseModel, Field

from . import DiscountEnum
from .user_id import UserId


class UserBase(UserId):
    """
    Base user model with common attributes.
    """

    full_name: str | None = Field(
        None,
        max_length=225,
        description="User's full name (first name and last name)",
    )
    username: str | None = Field(
        None,
        min_length=4,
        max_length=32,
        description="User's username",
    )
    language_code: str = Field(
        ...,
        max_length=3,
        description="IETF language tag of the user's language",
    )


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """

    pass


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    """

    full_name: str | None = Field(
        None,
        max_length=225,
        description="User's full name (first name and last name)",
    )
    username: str | None = Field(
        None,
        min_length=4,
        max_length=32,
        description="User's username",
    )
    language_code: str | None = Field(
        None,
        max_length=3,
        description="IETF language tag of the user's language",
    )
    last_activity_datetime: datetime = Field(
        ..., description="Time of last user activity"
    )
    base_balance: int | None = Field(None, description="User's base balance")


class UserSchema(UserBase):
    """
    Detailed user schema.
    """

    registration_datetime: datetime = Field(
        ..., description="Time of first user activity"
    )
    last_activity_datetime: datetime = Field(
        ..., description="Time of last user activity"
    )
    base_balance: int = Field(..., description="User's base balance")
    is_admin: bool = Field(..., description="True, if the user is an admin")
    is_blacklisted: bool = Field(..., description="True, if the user is blacklisted")
    is_premium: bool = Field(
        ..., description="True, if the user is a Book_base Premium user"
    )
    has_discount: bool | DiscountEnum = Field(
        ...,
        description="False, if the user does not have a discount or the discount value",
    )
