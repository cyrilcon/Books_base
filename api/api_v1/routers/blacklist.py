from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_user_by_id_depend
from api.api_v1.schemas import UserSchema, UserId
from config import config
from database import db_helper
from database.models import User

blacklist_router = APIRouter(
    prefix=config.api.v1.users + config.api.v1.blacklist,
    tags=[config.api.tags.blacklist],
)


@blacklist_router.get(
    "",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    summary="Get a list of blacklisted user IDs",
    response_description="List of blacklisted user IDs was successfully received.",
)
async def get_blacklisted_user_ids(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[int]:
    """
    Get a list of blacklisted user IDs.
    """

    return await crud.blacklist.get_blacklisted_user_ids(session=session)


@blacklist_router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Add a user to the blacklist",
    response_description="The user was successfully added to the blacklist.",
)
async def create_blacklist(
    user_id: UserId,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Add a user to the blacklist:

    - **id_user**: Unique user identifier
    """

    return await crud.blacklist.create_blacklist(session=session, user_id=user_id)


@blacklist_router.delete(
    "/{id_user}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a user from the blacklist",
    response_description="The user was successfully removed from the blacklist.",
)
async def delete_blacklist(
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Remove a user from the blacklist.
    """

    await crud.blacklist.delete_blacklist(session=session, id_user=user.id_user)
