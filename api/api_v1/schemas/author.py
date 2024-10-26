from typing import List

from pydantic import BaseModel, Field, model_validator


class AuthorBase(BaseModel):
    """
    Base author model with common attributes.
    """

    author_name: str = Field(..., max_length=255, description="Name of the author")


class AuthorCreate(AuthorBase):
    """
    Schema for creating a new author.
    """

    @model_validator(mode="before")
    def check_double_quote_in_author_name(cls, values):
        if '"' in values.get("author_name"):
            raise ValueError(
                'The author name must not contain the double quote (") character!!'
            )
        return values


class AuthorUpdate(AuthorBase):
    """
    Schema for updating author information.
    """

    author_name: str | None = Field(
        None, max_length=255, description="Name of the author"
    )

    @model_validator(mode="before")
    def check_double_quote_in_author_name(cls, values):
        if "author_name" in values and '"' in values.get("author_name"):
            raise ValueError(
                'The author name must not contain the double quote (") character!!'
            )
        return values


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
