from typing import Annotated

from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.schemas import AuthorSearchResponse, AuthorSchema
from config import config
from database import db_helper
from database.models import Author

authors_router = APIRouter(
    prefix=config.api.v1.authors,
    tags=[config.api.tags.authors],
)


@authors_router.get(
    "/search",
    response_model=AuthorSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search author using Levenshtein distance",
    response_description="The authors were successfully received by name similarity.",
)
async def search_authors(
    author_name: Annotated[
        str, Query(max_length=255, description="Name of the author to search for")
    ],
    max_results: Annotated[
        int, Query(ge=1, le=10, description="Maximum number of authors to return")
    ] = 5,
    similarity_threshold: Annotated[
        int, Query(ge=0, le=100, description="Minimum similarity threshold")
    ] = 75,
    page: Annotated[
        int | None, Query(ge=1, description="Page number for pagination")
    ] = None,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> AuthorSearchResponse:
    """
    Search authors with Levenshtein distance:

    - **found**: Number of authors found by search
    - **authors**: List of authors found:
        - **levenshtein_distance**: Similarity of the author by Levenshtein distance
        - **author**: Detailed author schema:
            - **id_author**: Unique author identifier
            - **author_name**: Name of the author
    """

    return await crud.authors.search_authors_with_similarity(
        session=session,
        author_name=author_name,
        max_results=max_results,
        similarity_threshold=similarity_threshold,
        page=page,
    )


@authors_router.get(
    "/{id_author}",
    response_model=AuthorSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an author by ID",
    response_description="The author was successfully received by ID.",
)
async def get_author_by_id(
    id_author: Annotated[int, Path(description="Unique author identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Author:
    """
    Get an author by ID:

    - **id_author**: Unique author identifier
    - **author_name**: Name of the author
    """

    author = await crud.authors.get_author_by_id(session=session, id_author=id_author)

    if author:
        return author
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Author with ID {id_author} not found!!",
    )
