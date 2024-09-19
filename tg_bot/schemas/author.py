from typing import List

from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    """
    Base author model with common attributes.
    """

    author_name: str = Field(..., max_length=255, description="Name of the author")


class AuthorCreate(AuthorBase):
    """
    Schema for creating a new author.
    """

    pass


class AuthorUpdate(AuthorBase):
    """
    Schema for updating author information.
    """

    author_name: str | None = Field(
        None, max_length=255, description="Name of the author"
    )


class AuthorSchema(BaseModel):
    """
    Detailed author schema.
    """

    id_author: int = Field(..., description="Unique author identifier")
    author_name: str = Field(..., max_length=255, description="Name of the author")


class AuthorSearchResult(BaseModel):
    """
    Schema for authors found with Levenshtein distance.
    """

    levenshtein_distance: float = Field(
        ..., description="Similarity of the author by Levenshtein distance"
    )
    author: AuthorSchema = Field(..., description="Detailed author schema")


class AuthorSearchResponse(BaseModel):
    """
    Response schema for authors found.
    """

    found: int = Field(..., description="Number of authors found by search")
    authors: List[AuthorSearchResult] = Field(..., description="List of authors found")
