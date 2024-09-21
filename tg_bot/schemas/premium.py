from pydantic import BaseModel, Field


class PremiumBase(BaseModel):
    """
    Base premium model with common attributes.
    """

    id_user: int = Field(..., description="Unique premium user identifier")


class PremiumCreate(PremiumBase):
    """
    Schema for assigning a user to premium.
    """

    pass
