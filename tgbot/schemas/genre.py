from typing import List

from pydantic import BaseModel, Field


class GenreBase(BaseModel):
    """
    Base genre model with common attributes.
    """

    genre_name: str = Field(..., max_length=255, description="Name of the genre")


class GenreCreate(GenreBase):
    """
    Schema for creating a new genre.
    """

    pass


class GenreUpdate(GenreBase):
    """
    Schema for updating genre information.
    """

    genre_name: str | None = Field(
        None, max_length=255, description="Name of the genre"
    )


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
