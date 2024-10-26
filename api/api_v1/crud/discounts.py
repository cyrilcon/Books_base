from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_user_details
from api.api_v1.schemas import UserSchema, DiscountCreate
from database.models import Discount, User


async def create_discount(
    session: AsyncSession, discount_data: DiscountCreate
) -> UserSchema:
    """
    Give a discount to the user.
    """

    user = await session.get(User, discount_data.id_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {discount_data.id_user} not found!!",
        )

    discount = Discount(**discount_data.model_dump())
    try:
        session.add(discount)
        await session.commit()
        user_details = await get_user_details(session, id_user=discount.id_user)
        return user_details
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {discount.id_user} already has a discount!!",
        )


async def delete_discount(session: AsyncSession, id_user: int) -> None:
    """
    Remove a discount from the user.
    """

    discount = await session.get(Discount, id_user)
    if not discount:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {id_user} already has no discount!!",
        )

    await session.delete(discount)
    await session.commit()
