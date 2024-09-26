from enum import Enum

from pydantic import BaseModel, Field


class DiscountEnum(int, Enum):
    """
    Available discount values.
    """

    FIFTEEN: int = 15
    THIRTY: int = 30
    FIFTY: int = 50
    HUNDRED: int = 100


class DiscountBase(BaseModel):
    """
    Base discount model with common attributes.
    """

    id_user: int = Field(..., description="Unique user identifier")
    discount_value: DiscountEnum = Field(..., description="Discount value")


class DiscountCreate(DiscountBase):
    """
    Schema for giving a discount to the user.
    """

    pass
