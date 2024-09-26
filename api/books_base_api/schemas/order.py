from datetime import datetime

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    """
    Base order model with common attributes.
    """

    id_order: int = Field(..., description="Unique order identifier")
    id_user: int = Field(..., description="Unique user identifier who made the order")
    book_title: str = Field(
        ...,
        max_length=255,
        description="Title of the book being ordered",
    )
    author_name: str = Field(
        ...,
        max_length=255,
        description="The author of the book being ordered",
    )


class OrderCreate(OrderBase):
    """
    Schema for creating a new order.
    """

    pass


class OrderSchema(OrderBase):
    """
    Detailed order schema.
    """

    order_datetime: datetime = Field(..., description="Time of order creation")
