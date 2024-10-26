from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_user_by_id_depend
from api.api_v1.schemas import UserSchema, UserId
from config import config
from database import db_helper
from database.models import User

admins_router = APIRouter(
    prefix=config.api.v1.users + config.api.v1.admins,
    tags=[config.api.tags.admins],
)


@admins_router.get(
    "",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    summary="Get a list of admin IDs",
    response_description="List of admin IDs was successfully received.",
)
async def get_admin_ids(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[int]:
    """
    Get a list of admin user IDs.
    """

    return await crud.admins.get_admin_ids(session=session)


@admins_router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add a user to admins",
    response_description="The user was successfully added to the admins.",
)
async def create_admin(
    user_id: UserId,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Create an admin:

    - **id_user**: Unique user identifier
    """

    return await crud.admins.create_admin(session=session, user_id=user_id)


@admins_router.delete(
    "/{id_user}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a user from admins",
    response_description="The user was successfully removed from the admins.",
)
async def delete_admin(
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Remove a user from the list of admins.
    """

    await crud.admins.delete_admin(session=session, id_user=user.id_user)
