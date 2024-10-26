from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas import OrderCreate
from database.models import Order, User


async def get_order_ids(session: AsyncSession) -> List[int]:
    """
    Get a list of order IDs.
    """

    stmt = select(Order.id_order)
    result: Result = await session.execute(stmt)
    order_ids = result.scalars().all()
    return list(order_ids)


async def create_order(session: AsyncSession, order_data: OrderCreate) -> Order:
    """
    Create a new order.
    """

    user = await session.get(User, order_data.id_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {order_data.id_user} not found!!",
        )

    order = Order(**order_data.model_dump())
    try:
        session.add(order)
        await session.commit()
        await session.refresh(order)
        return order
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Order with ID {order.id_order} already exists!!",
        )


async def get_order_by_position(session: AsyncSession, position: int) -> Order | None:
    """
    Get an order by position in the database.
    """

    stmt = (
        select(Order)
        .order_by(Order.order_datetime, Order.id_order)
        .offset(position - 1)
        .limit(1)
    )
    result: Result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    return order


async def get_orders_count(session: AsyncSession) -> int:
    """
    Get the total number of orders.
    """

    stmt = select(func.count(Order.id_order))
    result: Result = await session.execute(stmt)
    orders_count = result.scalar_one()
    return orders_count


async def get_order_by_id(session: AsyncSession, id_order: int) -> Order | None:
    """
    Get an order by ID.
    """

    stmt = select(Order).where(Order.id_order == id_order)
    result: Result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    return order


async def delete_order(session: AsyncSession, order: Order) -> None:
    """
    Cancel an order.
    """

    await session.delete(order)
    await session.commit()
