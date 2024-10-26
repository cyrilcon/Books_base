from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from database import db_helper
from database.models import Order


async def get_order_by_id_depend(
    id_order: Annotated[int, Path(description="Unique order identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Order:
    """
    Get an order by ID.
    """

    order = await crud.orders.get_order_by_id(session=session, id_order=id_order)
    if order:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order with ID {id_order} not found!!",
    )
