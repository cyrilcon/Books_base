from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_user_by_id_depend
from api.api_v1.schemas import UserSchema, DiscountCreate
from config import config
from database import db_helper
from database.models import User

discounts_router = APIRouter(
    prefix=config.api.v1.users + config.api.v1.discounts,
    tags=[config.api.tags.discounts],
)


@discounts_router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Give a discount to the user",
    response_description="The user was successfully given a discount.",
)
async def create_discount(
    discount_data: DiscountCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserSchema:
    """
    Give a discount to the user.
    """

    return await crud.discounts.create_discount(
        session=session, discount_data=discount_data
    )


@discounts_router.delete(
    "/{id_user}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remove a discount from the user",
    response_description="The discount was successfully removed from the user.",
)
async def delete_discount(
    user: User = Depends(get_user_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Remove a discount from the user.
    """

    await crud.discounts.delete_discount(session=session, id_user=user.id_user)
