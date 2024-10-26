from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_user_details
from api.api_v1.schemas import UserSchema, UserId
from database.models import User, Blacklist


async def get_blacklisted_user_ids(session: AsyncSession) -> List[int]:
    """
    Get a list of blacklisted user IDs.
    """

    stmt = select(Blacklist.id_user)
    result: Result = await session.execute(stmt)
    blacklisted_user_ids = result.scalars().all()
    return list(blacklisted_user_ids)


async def create_blacklist(session: AsyncSession, user_id: UserId) -> UserSchema:
    """
    Add a user to the blacklist.
    """

    user = await session.get(User, user_id.id_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id.id_user} not found!!",
        )

    blacklist = Blacklist(**user_id.model_dump())
    try:
        session.add(blacklist)
        await session.commit()
        user_details = await get_user_details(session, id_user=blacklist.id_user)
        return user_details
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {blacklist.id_user} is already blacklisted!!",
        )


async def delete_blacklist(session: AsyncSession, id_user: int) -> None:
    """
    Get a user from the blacklist.
    """

    blacklist = await session.get(Blacklist, id_user)
    if not blacklist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {id_user} is not blacklisted!!",
        )

    await session.delete(blacklist)
    await session.commit()
