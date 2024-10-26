from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_user_details
from api.api_v1.schemas import UserSchema, PremiumCreate
from database.models import Premium, User


async def create_premium(
    session: AsyncSession, premium_data: PremiumCreate
) -> UserSchema:
    """
    Assign a user to premium.
    """

    user = await session.get(User, premium_data.id_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {premium_data.id_user} not found!!",
        )

    premium = Premium(**premium_data.model_dump())
    try:
        session.add(premium)
        await session.commit()
        user_details = await get_user_details(session, id_user=premium.id_user)
        return user_details
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {premium.id_user} already has premium!!",
        )


async def delete_premium(session: AsyncSession, id_user: int) -> None:
    """
    Remove a user from the list of premium users.
    """

    premium = await session.get(Premium, id_user)
    if not premium:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {id_user} is not assigned to premium!!",
        )

    await session.delete(premium)
    await session.commit()
