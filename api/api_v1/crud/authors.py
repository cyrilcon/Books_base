from typing import List

from rapidfuzz import process, fuzz
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas import (
    AuthorCreate,
    AuthorUpdate,
    AuthorSchema,
    AuthorSearchResult,
    AuthorSearchResponse,
)
from database.models import Author, Book, BookAuthor


async def _get_all_authors(session: AsyncSession) -> List[AuthorSchema] | None:
    """
    Helper function to get all authors.
    """

    stmt = select(Author.id_author, Author.author_name)
    result: Result = await session.execute(stmt)
    authors = result.fetchall()
    if not authors:
        return None
    return [
        AuthorSchema(id_author=author.id_author, author_name=author.author_name)
        for author in authors
    ]


async def _get_author_by_name(session: AsyncSession, author_name: str) -> Author | None:
    """
    Helper function to get an author by name.
    """

    stmt = select(Author).where(Author.author_name == author_name)
    result: Result = await session.execute(stmt)
    author = result.scalar_one_or_none()
    return author


async def create_author(session: AsyncSession, author_data: AuthorCreate) -> Author:
    """
    Create a new author.
    """

    author = await _get_author_by_name(session, author_data.author_name)
    if author:
        return author

    author = Author(**author_data.model_dump())
    session.add(author)
    await session.commit()
    return author


async def search_authors_with_similarity(
    session: AsyncSession,
    author_name: str,
    max_results: int,
    similarity_threshold: int,
    page: int | None,
) -> AuthorSearchResponse:
    """
    Search authors with Levenshtein distance.
    """

    authors = await _get_all_authors(session=session)
    if not authors:
        return AuthorSearchResponse(found=0, authors=[])

    author_names = [author.author_name for author in authors]

    matching_authors = process.extract(
        author_name,
        author_names,
        scorer=fuzz.partial_ratio,
        limit=None,
    )

    matching_authors = [
        (match[0], match[1])
        for match in matching_authors
        if match[1] >= similarity_threshold
    ]

    found_authors_count = len(matching_authors)

    matching_ids = [
        authors[author_names.index(match[0])].id_author for match in matching_authors
    ]

    if not matching_ids:
        return AuthorSearchResponse(found=0, authors=[])

    search_response_authors = [
        AuthorSearchResult(
            levenshtein_distance=round(match[1], 2),
            author=authors[author_names.index(match[0])],
        )
        for match in matching_authors
    ]

    if page:
        start = (page - 1) * max_results
        end = start + max_results
        search_response_authors = search_response_authors[start:end]
    else:
        search_response_authors = search_response_authors[:max_results]

    return AuthorSearchResponse(
        found=found_authors_count, authors=search_response_authors
    )


async def get_author_by_id(session: AsyncSession, id_author: int) -> Author | None:
    """
    Get an author by ID.
    """

    stmt = select(Author).where(Author.id_author == id_author)
    result: Result = await session.execute(stmt)
    author = result.scalar_one_or_none()
    return author


async def update_book_authors(
    session: AsyncSession, book: Book, authors_update: list[AuthorUpdate]
):
    """
    Update the authors related to the book.
    """

    current_authors = {
        book_author.author.id_author: book_author for book_author in book.authors
    }
    new_author_ids = set()

    for author_data in authors_update:
        author_create_data = AuthorCreate(**author_data.model_dump())
        author = await create_author(session, author_create_data)
        new_author_ids.add(author.id_author)
        if author.id_author not in current_authors:
            book_author = BookAuthor(author=author, book=book)
            session.add(book_author)

    # Delete those authors who are not in the new data
    for author_id in list(current_authors.keys()):
        if author_id not in new_author_ids:
            await session.delete(current_authors[author_id])

    await session.commit()

    # Delete unused authors
    for author_id in list(current_authors.keys()):
        if author_id not in new_author_ids:
            await delete_author_if_unlinked(session, author_id)


async def delete_author_if_unlinked(session: AsyncSession, id_author: int) -> None:
    """
    Delete the author if they are not linked to any books.
    """

    stmt = select(BookAuthor).where(BookAuthor.id_author == id_author)
    result: Result = await session.execute(stmt)
    if not result.scalars().all():
        author = await session.get(Author, id_author)
        await session.delete(author)
        await session.commit()
