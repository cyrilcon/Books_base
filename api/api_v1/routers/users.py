from typing import List, Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_user_by_id_depend
from api.api_v1.schemas import UserSchema, UserCreate, UserUpdate, UserStats
from config import config
from database import db_helper
from database.models import User

users_router = APIRouter(
    prefix=config.api.v1.users,
    tags=[config.api.tags.users],
)


@users_router.get(
    "",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    summary="Get a list of user IDs",
    response_description="List of user IDs was successfully received.",
)
async def get_user_ids(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[int]:
    """
    Get a list of user IDs.
    """

    return await crud.users.get_user_ids(session=session)


@users_router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    response_description="The user was successfully created.",
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Create a user:

    - **id_user**: Unique user identifier
    - **full_name**: User's full name (first name and last name) | None
    - **username**: User's username | None
    - **language_code**: IETF language tag of the user's language
    """

    return await crud.users.create_user(session=session, user_data=user_data)


@users_router.get(
    "/stats",
    response_model=UserStats,
    status_code=status.HTTP_200_OK,
    summary="Get user activity statistics",
    response_description="User activity statistics were successfully received.",
)
async def get_user_statistics(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserStats:
    """
    Get user activity statistics:

    - **active_last_hour**: Number of users active in the last hour.
    - **active_last_24_hours**: Number of users active in the last 24 hours.
    - **active_last_week**: Number of users active in the last week.
    - **active_last_month**: Number of users active in the last month.
    - **total_users**: Total number of users in the database.
    """

    return await crud.users.get_user_statistics(session=session)


@users_router.get(
    "/username/{username}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a user by username",
    response_description="The user was successfully received by username.",
)
async def get_user_by_username(
    username: Annotated[
        str, Path(description="User's username", min_length=4, max_length=32)
    ],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Get a user by username:

    - **id_user**: Unique user identifier
    - **full_name**: User's full name (first name and last name) | None
    - **username**: User's username | None
    - **language_code**: IETF language tag of the user's language
    - **registration_datetime**: Time of first user activity
    - **last_activity_datetime**: Time of last user activity
    - **base_balance**: User's base balance
    - **is_admin**: True, if the user is an admin
    - **is_blacklisted**: True, if the user is blacklisted
    - **is_premium**: True, if the user is a Book_base Premium user
    - **has_discount**: False, if the user does not have a discount or the discount value
    """

    user = await crud.users.get_user_details(session=session, username=username)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with username '@{username}' not found!!",
    )


@users_router.get(
    "/{id_user}/books",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    summary="Get a list of book purchased IDs by the user",
    response_description="List of book purchased IDs was successfully received.",
)
async def get_book_ids(
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[int]:
    """
    Get a list of book purchased IDs by the user.
    """

    return await crud.users.get_book_ids(session=session, id_user=user.id_user)


@users_router.get(
    "/{id_user}/orders",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    summary="Get a list of order IDs by the user",
    response_description="List of order IDs was successfully received.",
)
async def get_order_ids_by_user(
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[int]:
    """
    Get a list of order IDs by the user.
    """

    return await crud.users.get_order_ids_by_user(session=session, id_user=user.id_user)


@users_router.get(
    "/{id_user}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a user by ID",
    response_description="The user was successfully received by ID.",
)
async def get_user_by_id(
    id_user: Annotated[int, Path(description="Unique user identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Get a user by ID:

    - **id_user**: Unique user identifier
    - **full_name**: User's full name (first name and last name) | None
    - **username**: User's username | None
    - **language_code**: IETF language tag of the user's language
    - **registration_datetime**: Time of first user activity
    - **last_activity_datetime**: Time of last user activity
    - **base_balance**: User's base balance
    - **is_admin**: True, if the user is an admin
    - **is_blacklisted**: True, if the user is blacklisted
    - **is_premium**: True, if the user is a Book_base Premium user
    - **has_discount**: False, if the user does not have a discount or the discount value
    """

    user = await crud.users.get_user_details(session=session, id_user=id_user)

    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id_user} not found!!",
    )


@users_router.patch(
    "/{id_user}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    response_description="The user was successfully updated.",
)
async def update_user(
    user_update_data: UserUpdate,
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Partially update user information:

    - **full_name**: User's full name (first name and last name) | None
    - **username**: User's username | None
    - **language_code**: IETF language tag of the user's language
    - **last_activity_datetime**: Time of last user activity
    - **base_balance**: User's base balance | None
    """

    return await crud.users.update_user(
        session=session,
        user=user,
        user_update_data=user_update_data,
    )
