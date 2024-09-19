from enum import Enum

from pydantic import BaseModel, Field


class DiscountEnum(int, Enum):
    """
    Available discount values.
    """

    FIFTEEN = 15
    THIRTY = 30
    FIFTY = 50
    HUNDRED = 100


class DiscountBase(BaseModel):
    """
    Base discount model with common attributes.
    """

    id_user: int = Field(..., description="Unique user identifier")
    discount: DiscountEnum = Field(..., description="Discount value")


class DiscountCreate(DiscountBase):
    """
    Schema for giving a discount to the user.
    """

    pass
