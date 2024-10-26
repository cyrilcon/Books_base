from typing import List, Annotated

from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.schemas import GenreSearchResponse, GenreSchema
from config import config
from database import db_helper
from database.models import Genre

genres_router = APIRouter(
    prefix=config.api.v1.genres,
    tags=[config.api.tags.genres],
)


@genres_router.get(
    "",
    response_model=List[GenreSchema],
    status_code=status.HTTP_200_OK,
    summary="Get a list of genres with pagination",
    response_description="List of genres was successfully received.",
)
async def get_genres_with_pagination(
    max_results: Annotated[
        int, Query(ge=1, le=10, description="Maximum number of genres to return")
    ] = 5,
    page: Annotated[
        int | None, Query(ge=1, description="Page number for pagination")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> List[Genre]:
    """
    Get a list of genres with pagination:

    - **id_genre**: Unique genre identifier
    - **genre_name**: Name of the genre
    """

    return await crud.genres.get_genres_with_pagination(
        session=session,
        max_results=max_results,
        page=page,
    )


@genres_router.get(
    "/count",
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary="Get the total number of genres",
    response_description="The total number of genres was successfully received.",
)
async def get_genres_count(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> int:
    """
    Get the total number of genres.
    """

    return await crud.genres.get_genres_count(session=session)


@genres_router.get(
    "/search",
    response_model=GenreSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search genre using Levenshtein distance",
    response_description="The genres were successfully received by name similarity.",
)
async def search_genres(
    genre_name: Annotated[
        str, Query(max_length=255, description="Name of the genre to search for")
    ],
    max_results: Annotated[
        int, Query(ge=1, le=10, description="Maximum number of genres to return")
    ] = 5,
    similarity_threshold: Annotated[
        int, Query(ge=0, le=100, description="Minimum similarity threshold")
    ] = 75,
    page: Annotated[
        int | None, Query(ge=1, description="Page number for pagination")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> GenreSearchResponse:
    """
    Search genres with Levenshtein distance:

    - **found**: Number of genres found by search
    - **genres**: List of genres found:
        - **levenshtein_distance**: Similarity of the genre by Levenshtein distance
        - **genre**: Detailed genre schema:
            - **id_genre**: Unique genre identifier
            - **genre_name**: Name of the genre
    """

    return await crud.genres.search_genres_with_similarity(
        session=session,
        genre_name=genre_name,
        max_results=max_results,
        similarity_threshold=similarity_threshold,
        page=page,
    )


@genres_router.get(
    "/{id_genre}",
    response_model=GenreSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a genre by ID",
    response_description="The genre was successfully received by ID.",
)
async def get_author_by_id(
    id_genre: Annotated[int, Path(description="Unique genre identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Genre:
    """
    Get a genre by ID:

    - **id_genre**: Unique genre identifier
    - **genre_name**: Name of the genre
    """

    genre = await crud.genres.get_genre_by_id(session=session, id_genre=id_genre)

    if genre:
        return genre
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Genre with ID {id_genre} not found!!",
    )
