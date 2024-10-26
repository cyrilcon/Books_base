from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, model_validator

from api.api_v1.schemas import BookSchema


class PaymentCurrencyEnum(str, Enum):
    """
    Available payment currency values.
    """

    XTR: str = "XTR"
    RUB: str = "RUB"


class PaymentTypeEnum(str, Enum):
    """
    Available payment type values.
    """

    BOOK: str = "book"
    PREMIUM: str = "premium"


class PaymentBase(BaseModel):
    """
    Base payment model with common attributes.
    """

    id_payment: str = Field(..., description="Unique payment identifier")
    id_user: int = Field(..., description="Unique user identifier who made the payment")
    price: int = Field(..., description="Price of payment")
    currency: PaymentCurrencyEnum = Field(
        ..., description="Currency in which the payment was made"
    )
    type: PaymentTypeEnum = Field(
        ..., description="Payment type value (what was purchased)"
    )


class PaymentCreate(PaymentBase):
    """
    Schema for creating a new payment.
    """

    book_ids: List[int] | None = Field(
        None, description="List of unique book identifiers (articles of the books)"
    )

    @model_validator(mode="before")
    def check_book_ids_for_book_type(cls, values):
        if values.get("type") == "book" and not values.get("book_ids"):
            raise ValueError("For 'book' payment type, 'book_ids' must be provided!!")
        if values.get("type") == "premium" and "book_ids" in values:
            raise ValueError(
                "For 'premium' payment type, 'book_ids' must not be provided!!"
            )
        return values


class PaymentSchema(PaymentBase):
    """
    Detailed payment schema.
    """

    books: List[BookSchema] | None = Field(None, description="List of books purchased")
    payment_datetime: datetime = Field(..., description="Time of payment creation")
