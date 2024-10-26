from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.schemas import PaymentCreate, PaymentSchema
from config import config
from database import db_helper

payments_router = APIRouter(
    prefix=config.api.v1.payments,
    tags=[config.api.tags.payments],
)


@payments_router.post(
    "",
    response_model=PaymentSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create a payment",
    response_description="The payment was successfully created.",
)
async def create_payment(
    payment_data: PaymentCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> PaymentSchema:
    """
    Create a payment:

    - **id_payment**: Unique payment identifier
    - **id_user**: Unique user identifier who made the payment
    - **price**: Price of payment
    - **currency**: Currency in which the payment was made
    - **type**: Payment type value (what was purchased)
    - (**book_ids**: Currency in which the payment was made)
    """

    return await crud.payments.create_payment(
        session=session, payment_data=payment_data
    )


@payments_router.get(
    "/{id_payment}",
    response_model=PaymentSchema,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    summary="Get a payment by ID",
    response_description="The payment was successfully received by ID.",
)
async def get_payment_by_id(
    id_payment: Annotated[str, Path(description="Unique payment identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> PaymentSchema:
    """
    Get a payment by ID:

    - **id_payment**: Unique payment identifier
    - **id_user**: Unique user identifier who made the payment
    - **price**: Price of payment
    - **currency**: Currency in which the payment was made
    - **type**: Payment type value (what was purchased)
    - (**books**: List of books purchased)
    - **payment_datetime**: Time of payment creation
    """

    payment = await crud.payments.get_payment_by_id(
        session=session, id_payment=id_payment
    )
    if payment:
        return payment
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Payment with ID {id_payment} not found!!",
    )
