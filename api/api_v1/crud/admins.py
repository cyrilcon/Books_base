from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.crud.users import get_user_details
from api.api_v1.schemas import UserSchema, UserId
from database.models import Admin, User


async def get_admin_ids(session: AsyncSession) -> List[int]:
    """
    Get a list of admin user IDs.
    """

    stmt = select(Admin.id_user)
    result: Result = await session.execute(stmt)
    admin_ids = result.scalars().all()
    return list(admin_ids)


async def create_admin(session: AsyncSession, user_id: UserId) -> UserSchema:
    """
    Create a new admin.
    """

    user = await session.get(User, user_id.id_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id.id_user} not found!!",
        )

    admin = Admin(**user_id.model_dump())
    try:
        session.add(admin)
        await session.commit()
        user_details = await get_user_details(session, id_user=admin.id_user)
        return user_details
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {admin.id_user} is already an admin!!",
        )


async def delete_admin(session: AsyncSession, id_user: int) -> None:
    """
    Remove a user from the list of admins.
    """

    admin = await session.get(Admin, id_user)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with ID {id_user} is not an admin!!",
        )

    await session.delete(admin)
    await session.commit()
