from enum import Enum


class DiscountEnum(int, Enum):
    """
    Available discount values.
    """

    FIFTEEN = 15
    THIRTY = 30
    FIFTY = 50
    HUNDRED = 100
