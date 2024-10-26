from typing import Annotated, List

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_order_by_id_depend
from api.api_v1.schemas import OrderCreate, OrderSchema
from config import config
from database import db_helper
from database.models import Order

orders_router = APIRouter(
    prefix=config.api.v1.orders,
    tags=[config.api.tags.orders],
)


@orders_router.get(
    "",
    response_model=List[int],
    status_code=status.HTTP_200_OK,
    summary="Get a list of order IDs",
    response_description="List of order IDs was successfully received.",
)
async def get_order_ids(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[int]:
    """
    Get a list of order IDs.
    """

    return await crud.orders.get_order_ids(session=session)


@orders_router.post(
    "",
    response_model=OrderSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create an order",
    response_description="The order was successfully created.",
)
async def create_order(
    order_data: OrderCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Order:
    """
    Create an order:

    - **id_order**: Unique order identifier
    - **id_user**: Unique user identifier who made the order
    - **book_title**: Title of the book being ordered
    - **author_name**: The author of the book being ordered
    """

    return await crud.orders.create_order(session=session, order_data=order_data)


@orders_router.get(
    "/count",
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary="Get the total number of orders",
    response_description="The total number of orders was successfully received.",
)
async def get_orders_count(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> int:
    """
    Get the total number of orders.
    """

    return await crud.orders.get_orders_count(session=session)


@orders_router.get(
    "/position/{position}",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an order by position in the database",
    response_description="The order was successfully received by position in the database.",
)
async def get_order_by_position(
    position: Annotated[int, Path(description="Order position in the database")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Order:
    """
    Get an order by position in the database:

    - **id_order**: Unique order identifier
    - **id_user**: Unique user identifier who made the order
    - **book_title**: Title of the book being ordered
    - **author_name**: The author of the book being ordered
    - **order_datetime**: Time of order creation
    """

    order = await crud.orders.get_order_by_position(session=session, position=position)

    if order:
        return order
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order at position {position} in the database not found!!",
    )


@orders_router.get(
    "/{id_order}",
    response_model=OrderSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an order by ID",
    response_description="The order was successfully received by ID.",
)
async def get_order_by_id(
    order: Order = Depends(get_order_by_id_depend),
) -> Order:
    """
    Get an order by ID:

    - **id_order**: Unique order identifier
    - **id_user**: Unique user identifier who made the order
    - **book_title**: Title of the book being ordered
    - **author_name**: The author of the book being ordered
    - **order_datetime**: Time of order creation
    """

    return order


@orders_router.delete(
    "/{id_order}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel an order",
    response_description="The order was successfully cancelled.",
)
async def delete_order(
    order: Order = Depends(get_order_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Cancel an order.
    """

    await crud.orders.delete_order(session=session, order=order)
