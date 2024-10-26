from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1 import crud
from api.api_v1.schemas import ArticleCreate, ArticleSchema
from config import config
from database import db_helper
from database.models import Article

articles_router = APIRouter(
    prefix=config.api.v1.articles,
    tags=[config.api.tags.articles],
)


@articles_router.post(
    "",
    response_model=ArticleSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create an article",
    response_description="The article was successfully created.",
)
async def create_article(
    article_data: ArticleCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Article:
    """
    Create an article:

    - **link**: Link to the Telegraph article
    - **title**: Title of the article
    - **language_code**: IETF language tag of the article
    """

    return await crud.articles.create_article(
        session=session, article_data=article_data
    )


@articles_router.get(
    "/link/{link:path}",
    response_model=ArticleSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an article by link",
    response_description="The article was successfully received by link.",
)
async def get_article_by_link(
    link: Annotated[
        str, Path(description="Link to the Telegraph article", max_length=255)
    ],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Article:
    """
    Get an article by link:

    - **id_article**: Unique article identifier
    - **link**: Link to the Telegraph article
    - **title**: Title of the article
    - **language_code**: IETF language tag of the article
    - **added_datetime**: Time of article addition
    """

    article = await crud.articles.get_article_by_link(session=session, link=link)

    if article:
        return article
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Article with such a link not found!!",
    )


@articles_router.get(
    "/{language_code}/count",
    response_model=int,
    status_code=status.HTTP_200_OK,
    summary="Get the total number of articles by language_code",
    response_description="The total number of articles by language_code was successfully received.",
)
async def get_articles_count_by_language_code(
    language_code: Annotated[str, Path(description="IETF language tag of the article")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> int:
    """
    Get the total number of articles by language_code.
    """

    return await crud.articles.get_articles_count_by_language_code(
        session=session, language_code=language_code
    )


@articles_router.get(
    "/{language_code}/position/{position}",
    response_model=ArticleSchema,
    status_code=status.HTTP_200_OK,
    summary="Get an article by language_code and position in the database",
    response_description="The article was successfully received by language_code and position in the database.",
)
async def get_article_by_language_code_and_position(
    language_code: Annotated[str, Path(description="IETF language tag of the article")],
    position: Annotated[int, Path(description="Article position in the database")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Article:
    """
    Get an article by language_code and position in the database:

    - **id_article**: Unique article identifier
    - **link**: Link to the Telegraph article
    - **title**: Title of the article
    - **language_code**: IETF language tag of the article
    - **added_datetime**: Time of article addition
    """

    article = await crud.articles.get_article_by_language_code_and_position(
        session=session,
        language_code=language_code,
        position=position,
    )

    if article:
        return article
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Article with language code '{language_code}' at position {position} in the database not found!!",
    )


@articles_router.delete(
    "/{id_article}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an article",
    response_description="The article was successfully deleted.",
)
async def delete_article(
    id_article: Annotated[int, Path(description="Unique article identifier")],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> None:
    """
    Delete an article.
    """

    article = await crud.articles.get_article_by_id(
        session=session, id_article=id_article
    )

    if article:
        return await crud.articles.delete_article(session=session, article=article)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Article with ID {id_article} not found!!",
    )
