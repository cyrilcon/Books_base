from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from tgbot.schemas.author import AuthorCreate, AuthorUpdate, AuthorSchema
from tgbot.schemas.file import FileCreate, FileUpdate, FileSchema
from tgbot.schemas.genre import GenreCreate, GenreUpdate, GenreSchema


class PriceEnum(int, Enum):
    """
    Available price values.
    """

    FIFTY = 50
    EIGHTY_FIVE = 85


class BookBase(BaseModel):
    """
    Base book model with common attributes.
    """

    id_book: int = Field(
        ..., description="Unique book identifier (article of the book)"
    )
    title: str = Field(
        ...,
        max_length=255,
        description="Title of the book",
    )
    cover: str = Field(
        ...,
        max_length=255,
        description="Token of the book cover image",
    )
    description: str = Field(..., description="Description of the book")
    price: PriceEnum = Field(..., description="Price of the book (50 or 85)")


class BookCreate(BookBase):
    """
    Schema for creating a new book.
    """

    authors: List[AuthorCreate] = Field(
        ..., description="List of authors associated with the book"
    )
    genres: List[GenreCreate] = Field(
        ..., description="List of genres associated with the book"
    )
    files: List[FileCreate] = Field(
        ..., description="List of files associated with the book"
    )


class BookUpdate(BookBase):
    """
    Schema for updating book information.
    """

    id_book: int | None = Field(
        None, description="Unique book identifier (article of the book)"
    )
    title: str | None = Field(
        None,
        max_length=255,
        description="Title of the book",
    )
    description: str | None = Field(None, description="Description of the book")
    cover: str | None = Field(
        None,
        max_length=255,
        description="Token of the book cover image",
    )
    price: PriceEnum | None = Field(None, description="Price of the book (50 or 85)")
    authors: List[AuthorUpdate] | None = Field(
        None, description="List of authors associated with the book"
    )
    genres: List[GenreUpdate] | None = Field(
        None, description="List of genres associated with the book"
    )
    files: List[FileUpdate] | None = Field(
        None, description="List of files associated with the book"
    )


class BookSchema(BookBase):
    """
    Detailed book schema.
    """

    authors: List[AuthorSchema] = Field(
        ..., description="List of authors associated with the book"
    )
    genres: List[GenreSchema] = Field(
        ..., description="List of genres associated with the book"
    )
    files: List[FileSchema] = Field(
        ..., description="List of files associated with the book"
    )
    added_datetime: datetime = Field(..., description="Time of book addition")


class BookIdTitle(BaseModel):
    """
    Book schema with id and title.
    """

    id_book: int = Field(
        ..., description="Unique book identifier (article of the book)"
    )
    title: str = Field(
        ...,
        max_length=255,
        description="Title of the book",
    )


class BookResult(BaseModel):
    """
    Schema representing a book result.
    """

    book: BookSchema = Field(..., description="Detailed book schema")


class BooksResponse(BaseModel):
    """
    General response schema for listing books.
    """

    count: int = Field(..., description="Number of books")
    books: List[BookResult] = Field(..., description="List of books received")


class BookTitleSimilarityResult(BaseModel):
    """
    Schema for books found by title with Levenshtein distance.
    """

    levenshtein_distance: float = Field(
        ..., description="Similarity of the book by Levenshtein distance"
    )
    book: BookSchema = Field(..., description="Detailed book schema")


class BookTitleSimilarityResponse(BaseModel):
    """
    Response schema for books found by title.
    """

    found: int = Field(..., description="Number of books found by search")
    books: List[BookTitleSimilarityResult] = Field(
        ..., description="List of books found"
    )
