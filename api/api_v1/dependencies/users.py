from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from database import db_helper
from database.models import User


async def get_user_by_id_depend(
    id_user: Annotated[int, Path(description="Unique user identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    """
    Get a user by ID.
    """

    user = await crud.users.get_user_by_id(session=session, id_user=id_user)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id_user} not found!!",
    )
