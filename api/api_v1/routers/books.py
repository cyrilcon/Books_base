from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.dependencies import get_book_by_id_depend
from api.api_v1.schemas import (
    BookCreate,
    BookUpdate,
    BookSchema,
    BooksResponse,
    BookTitleSimilarityResponse,
)
from config import config
from database import db_helper
from database.models import Book

books_router = APIRouter(
    prefix=config.api.v1.books,
    tags=[config.api.tags.books],
)


@books_router.post(
    "",
    response_model=BookSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a book",
    response_description="The book was successfully created.",
)
async def create_book(
    book_data: BookCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BookSchema:
    """
    Create a book:

    - **id_book**: Unique book identifier (article of the book)
    - **title**: Title of the book
    - **cover**: Token of the book cover image
    - **description**: Description of the book
    - **price**: Price of the book (50 or 85)
    - **authors**: List of authors associated with the book:
        - **author_name**: Name of the author
    - **genres**: List of genres associated with the book:
        - **genre_name**: Name of the genre
    - **files**: List of files associated with the book:
        - **format**: Format of the file
        - **file_token**: Token of the book file
    """

    return await crud.books.create_book_details(session=session, book_data=book_data)


@books_router.get(
    "/author/{id_author}",
    response_model=BooksResponse,
    status_code=status.HTTP_200_OK,
    summary="Get books by author ID",
    response_description="The books ware successfully received by author ID.",
)
async def get_books_by_author_id(
    id_author: Annotated[int, Path(description="Unique author identifier")],
    max_results: Annotated[
        int, Query(ge=1, le=10, description="Maximum number of books to return")
    ] = 5,
    page: Annotated[
        int | None, Query(ge=1, description="Page number for pagination")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BooksResponse:
    """
    Get books by author ID:

    - **count**: Number of books
    - **books**: List of books by the author:
        - **book**: Detailed book schema:
            - **id_book**: Unique book identifier (article of the book)
            - **title**: Title of the book
            - **cover**: Token of the book cover image
            - **description**: Description of the book
            - **price**: Price of the book (50 or 85)
            - **authors**: List of authors associated with the book:
                - **id_author**: Unique author identifier
                - **author_name**: Name of the author
            - **genres**: List of genres associated with the book:
                - **id_genre**: Unique genre identifier
                - **genre_name**: Name of the genre
            - **files**: List of files associated with the book:
                - **id_file**: Unique file identifier
                - **format**: Format of the file
                - **file_token**: Token of the book file
            - **added_datetime**: Time of book addition
    """

    return await crud.books.get_books_by_author_id(
        session=session,
        id_author=id_author,
        max_results=max_results,
        page=page,
    )


@books_router.get(
    "/genre/{id_genre}",
    response_model=BooksResponse,
    status_code=status.HTTP_200_OK,
    summary="Get books by genre ID",
    response_description="The books ware successfully received by genre ID.",
)
async def get_books_by_genre_id(
    id_genre: Annotated[int, Path(description="Unique genre identifier")],
    max_results: Annotated[
        int, Query(ge=1, le=10, description="Maximum number of books to return")
    ] = 5,
    page: Annotated[
        int | None, Query(ge=1, description="Page number for pagination")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BooksResponse:
    """
    Get books by genre ID:

    - **count**: Number of books
    - **books**: List of books by the genre:
        - **book**: Detailed book schema:
            - **id_book**: Unique book identifier (article of the book)
            - **title**: Title of the book
            - **cover**: Token of the book cover image
            - **description**: Description of the book
            - **price**: Price of the book (50 or 85)
            - **authors**: List of authors associated with the book:
                - **id_author**: Unique author identifier
                - **author_name**: Name of the author
            - **genres**: List of genres associated with the book:
                - **id_genre**: Unique genre identifier
                - **genre_name**: Name of the genre
            - **files**: List of files associated with the book:
                - **id_file**: Unique file identifier
                - **format**: Format of the file
                - **file_token**: Token of the book file
            - **added_datetime**: Time of book addition
    """

    return await crud.books.get_books_by_genre_id(
        session=session,
        id_genre=id_genre,
        max_results=max_results,
        page=page,
    )


@books_router.get(
    "/latest-article",
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary="Get the latest article",
    response_description="The latest article was successfully received.",
)
async def get_latest_article(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> int:
    """
    Get the latest article of books.
    """

    return await crud.books.get_latest_article(session=session)


@books_router.patch(
    "/price",
    response_model=BookSchema,
    status_code=status.HTTP_200_OK,
    summary="Update the book price to 85",
    response_description="Book price was successfully updated to 85.",
)
async def update_book_price(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BookSchema:
    """
    Update the price of the book with a price of 50 to 85.
    """

    return await crud.books.update_book_price(session=session)


@books_router.get(
    "/search-by-title",
    response_model=BookTitleSimilarityResponse,
    status_code=status.HTTP_200_OK,
    summary="Search books by title using Levenshtein distance",
    response_description="The books were successfully received by title similarity.",
)
async def search_books_by_title(
    title: Annotated[
        str, Query(max_length=255, description="Title of the book to search for")
    ],
    max_results: Annotated[
        int, Query(ge=1, le=10, description="Maximum number of books to return")
    ] = 5,
    similarity_threshold: Annotated[
        int, Query(ge=0, le=100, description="Minimum similarity threshold")
    ] = 75,
    page: Annotated[
        int | None, Query(ge=1, description="Page number for pagination")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BookTitleSimilarityResponse:
    """
    Search books by title with Levenshtein distance:

    - **found**: Number of books found by search
    - **books**: List of books found:
        - **levenshtein_distance**: Similarity of the book by Levenshtein distance
        - **book**: Detailed book schema:
            - **id_book**: Unique book identifier (article of the book)
            - **title**: Title of the book
            - **cover**: Token of the book cover image
            - **description**: Description of the book
            - **price**: Price of the book (50 or 85)
            - **authors**: List of authors associated with the book:
                - **id_author**: Unique author identifier
                - **author_name**: Name of the author
            - **genres**: List of genres associated with the book:
                - **id_genre**: Unique genre identifier
                - **genre_name**: Name of the genre
            - **files**: List of files associated with the book:
                - **id_file**: Unique file identifier
                - **format**: Format of the file
                - **file_token**: Token of the book file
            - **added_datetime**: Time of book addition
    """

    return await crud.books.search_books_by_title_with_similarity(
        session=session,
        title=title,
        max_results=max_results,
        similarity_threshold=similarity_threshold,
        page=page,
    )


@books_router.get(
    "/{id_book}",
    response_model=BookSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a book by ID",
    response_description="The book was successfully received by ID.",
)
async def get_book_by_id(
    id_book: Annotated[int, Path(description="Unique book identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BookSchema:
    """
    Get a book by ID:

    - **id_book**: Unique book identifier (article of the book)
    - **title**: Title of the book
    - **cover**: Token of the book cover image
    - **description**: Description of the book
    - **price**: Price of the book (50 or 85)
    - **authors**: List of authors associated with the book:
        - **id_author**: Unique author identifier
        - **author_name**: Name of the author
    - **genres**: List of genres associated with the book:
        - **id_genre**: Unique genre identifier
        - **genre_name**: Name of the genre
    - **files**: List of files associated with the book:
        - **id_file**: Unique file identifier
        - **format**: Format of the file
        - **file_token**: Token of the book file
    - **added_datetime**: Time of book addition
    """

    book = await crud.books.get_book_details(session=session, id_book=id_book)

    if book:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Book with ID {id_book} not found!!",
    )


@books_router.patch(
    "/{id_book}",
    response_model=BookSchema,
    status_code=status.HTTP_200_OK,
    summary="Update a book",
    response_description="The book was successfully updated.",
)
async def update_book(
    book_update_data: BookUpdate,
    book: Book = Depends(get_book_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BookSchema:
    """
    Partially update book information:

    - **id_book**: Unique book identifier (article of the book) | None
    - **title**: Title of the book | None
    - **cover**: Token of the book cover image | None
    - **description**: Description of the book | None
    - **price**: Price of the book (50 or 85) | None
    - **authors**: List of authors associated with the book:
        - **author_name**: Name of the author | None
    - **genres**: List of genres associated with the book:
        - **genre_name**: Name of the genre | None
    - **files**: List of files associated with the book:
        - **format**: Format of the file | None
        - **file_token**: Token of the book file | None
    """

    return await crud.books.update_book(
        session=session,
        book=book,
        book_update_data=book_update_data,
    )


@books_router.delete(
    "/{id_book}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    response_description="The book was successfully deleted.",
)
async def delete_book(
    book: Book = Depends(get_book_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Delete a book.
    """

    await crud.books.delete_book(session=session, book=book)


@books_router.delete(
    "/{id_book}/file/{file_format}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    response_description="The book was successfully deleted.",
)
async def delete_file(
    file_format: Annotated[str, Path(description="Format of the file")],
    book: Book = Depends(get_book_by_id_depend),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Delete a file of the book by its format.
    """

    await crud.books.delete_file(
        session=session,
        id_book=book.id_book,
        file_format=file_format,
    )
