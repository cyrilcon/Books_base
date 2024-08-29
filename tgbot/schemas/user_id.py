from pydantic import BaseModel, Field


class UserId(BaseModel):
    """
    Schema for representing a user ID.
    """

    id_user: int = Field(..., description="Unique user identifier")
