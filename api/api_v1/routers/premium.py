from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_user_by_id_depend
from api.api_v1.schemas import UserSchema, PremiumCreate
from config import config
from database import db_helper
from database.models import User

premium_router = APIRouter(
    prefix=config.api.v1.users + config.api.v1.premium,
    tags=[config.api.tags.premium],
)


@premium_router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Assign a user to premium",
    response_description="The user was successfully assigned to premium.",
)
async def create_premium(
    premium_data: PremiumCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Assign a user to premium.
    """

    return await crud.premium.create_premium(session=session, premium_data=premium_data)


@premium_router.delete(
    "/{id_user}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a user from premium",
    response_description="The user was successfully removed from premium.",
)
async def delete_premium(
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Remove a user from the list of premium users.
    """

    await crud.premium.delete_premium(session=session, id_user=user.id_user)
