from typing import List

from pydantic import BaseModel, Field, model_validator


class GenreBase(BaseModel):
    """
    Base genre model with common attributes.
    """

    genre_name: str = Field(..., max_length=255, description="Name of the genre")


class GenreCreate(GenreBase):
    """
    Schema for creating a new genre.
    """

    @model_validator(mode="before")
    def check_double_quote_in_genre_name(cls, values):
        if '"' in values.get("genre_name"):
            raise ValueError(
                'The genre name must not contain the double quote (") character!!'
            )
        return values


class GenreUpdate(GenreBase):
    """
    Schema for updating genre information.
    """

    genre_name: str | None = Field(
        None, max_length=255, description="Name of the genre"
    )

    @model_validator(mode="before")
    def check_double_quote_in_genre_name(cls, values):
        if "genre_name" in values and '"' in values.get("genre_name"):
            raise ValueError(
                'The genre name must not contain the double quote (") character!!'
            )
        return values


class GenreSchema(BaseModel):
    """
    Detailed genre schema.
    """

    id_genre: int = Field(..., description="Unique genre identifier")
    genre_name: str = Field(..., max_length=255, description="Name of the genre")


class GenreSearchResult(BaseModel):
    """
    Schema for genres found with Levenshtein distance.
    """

    levenshtein_distance: float = Field(
        ..., description="Similarity of the genre by Levenshtein distance"
    )
    genre: GenreSchema = Field(..., description="Detailed genre schema")


class GenreSearchResponse(BaseModel):
    """
    Response schema for genres found.
    """

    found: int = Field(..., description="Number of genres found by search")
    genres: List[GenreSearchResult] = Field(..., description="List of genres found")
