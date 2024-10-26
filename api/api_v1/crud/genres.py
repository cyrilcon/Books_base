from typing import List

from rapidfuzz import process, fuzz
from sqlalchemy import Result, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas import (
    GenreCreate,
    GenreUpdate,
    GenreSchema,
    GenreSearchResponse,
    GenreSearchResult,
)
from database.models import Genre, Book, BookGenre


async def _get_all_genres(session: AsyncSession) -> List[GenreSchema] | None:
    """
    Helper function to get all genres.
    """

    stmt = select(Genre.id_genre, Genre.genre_name)
    result: Result = await session.execute(stmt)
    genres = result.fetchall()
    if not genres:
        return None
    return [
        GenreSchema(id_genre=genre.id_genre, genre_name=genre.genre_name)
        for genre in genres
    ]


async def _get_genre_by_name(session: AsyncSession, genre_name: str) -> Genre | None:
    """
    Helper function to get a genre by name.
    """

    stmt = select(Genre).where(Genre.genre_name == genre_name)
    result: Result = await session.execute(stmt)
    genre = result.scalar_one_or_none()
    return genre


async def create_genre(session: AsyncSession, genre_data: GenreCreate) -> Genre:
    """
    Create a new genre.
    """

    genre_name_lower = genre_data.genre_name.lower()

    genre = await _get_genre_by_name(session, genre_name_lower)
    if genre:
        return genre

    genre = Genre(genre_name=genre_name_lower)
    session.add(genre)
    await session.commit()
    return genre


async def get_genres_with_pagination(
    session: AsyncSession,
    max_results: int,
    page: int | None,
) -> List[Genre]:
    """
    Get a list of genres with pagination.
    """

    # Calculate the offset depending on the page
    offset_value = (page - 1) * max_results if page else 0

    stmt = (
        select(Genre).order_by(Genre.genre_name).offset(offset_value).limit(max_results)
    )
    result: Result = await session.execute(stmt)
    genres = result.scalars().all()
    return list(genres)


async def get_genres_count(session: AsyncSession) -> int:
    """
    Get the total number of genres.
    """

    stmt = select(func.count(Genre.id_genre))
    result: Result = await session.execute(stmt)
    genres_count = result.scalar_one()
    return genres_count


async def search_genres_with_similarity(
    session: AsyncSession,
    genre_name: str,
    max_results: int,
    similarity_threshold: int,
    page: int | None,
) -> GenreSearchResponse:
    """
    Search genres with Levenshtein distance.
    """

    genres = await _get_all_genres(session=session)
    if not genres:
        return GenreSearchResponse(found=0, genres=[])

    genre_names = [genre.genre_name for genre in genres]

    matching_genres = process.extract(
        genre_name,
        genre_names,
        scorer=fuzz.partial_ratio,
        limit=None,
    )

    matching_genres = [
        (match[0], match[1])
        for match in matching_genres
        if match[1] >= similarity_threshold
    ]

    found_genres_count = len(matching_genres)

    matching_ids = [
        genres[genre_names.index(match[0])].id_genre for match in matching_genres
    ]

    if not matching_ids:
        return GenreSearchResponse(found=0, genres=[])

    search_response_genres = [
        GenreSearchResult(
            levenshtein_distance=round(match[1], 2),
            genre=genres[genre_names.index(match[0])],
        )
        for match in matching_genres
    ]

    if page:
        start = (page - 1) * max_results
        end = start + max_results
        search_response_genres = search_response_genres[start:end]
    else:
        search_response_genres = search_response_genres[:max_results]

    return GenreSearchResponse(found=found_genres_count, genres=search_response_genres)


async def get_genre_by_id(session: AsyncSession, id_genre: int) -> Genre | None:
    """
    Get a genre by ID.
    """

    stmt = select(Genre).where(Genre.id_genre == id_genre)
    result: Result = await session.execute(stmt)
    genre = result.scalar_one_or_none()
    return genre


async def update_book_genres(
    session: AsyncSession, book: Book, genres_update: list[GenreUpdate]
):
    """
    Update the genres related to the book.
    """

    current_genres = {
        book_genre.genre.id_genre: book_genre for book_genre in book.genres
    }
    new_genre_ids = set()

    for genre_data in genres_update:
        genre_create_data = GenreCreate(**genre_data.model_dump())
        genre = await create_genre(session, genre_create_data)
        new_genre_ids.add(genre.id_genre)
        if genre.id_genre not in current_genres:
            book_genre = BookGenre(genre=genre, book=book)
            session.add(book_genre)

    # Delete genres that are not in the new data
    for genre_id in list(current_genres.keys()):
        if genre_id not in new_genre_ids:
            await session.delete(current_genres[genre_id])

    await session.commit()

    # Deletes unused genres
    for genre_id in list(current_genres.keys()):
        if genre_id not in new_genre_ids:
            await delete_genre_if_unlinked(session, genre_id)


async def delete_genre_if_unlinked(session: AsyncSession, id_genre: int) -> None:
    """
    Delete the genre if it is not linked to any books.
    """

    stmt = select(BookGenre).where(BookGenre.id_genre == id_genre)
    result: Result = await session.execute(stmt)
    if not result.scalars().all():
        genre = await session.get(Genre, id_genre)
        await session.delete(genre)
        await session.commit()
