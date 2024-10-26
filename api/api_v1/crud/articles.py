from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.schemas import ArticleCreate
from database.models import Article


async def create_article(session: AsyncSession, article_data: ArticleCreate) -> Article:
    """
    Create a new article.
    """

    article = Article(
        link=str(article_data.link),
        title=article_data.title,
        language_code=article_data.language_code,
    )
    try:
        session.add(article)
        await session.commit()
        await session.refresh(article)
        return article
    except IntegrityError as e:
        if "link" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Article with such a link already exists!!",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Conflict in article data!!",
            )


async def get_article_by_link(session: AsyncSession, link: str) -> Article | None:
    """
    Get an article by link.
    """

    stmt = select(Article).where(Article.link == link)
    result: Result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    return article


async def get_articles_count_by_language_code(
    session: AsyncSession,
    language_code: str,
) -> int:
    """
    Get the total number of articles by language_code.
    """

    stmt = select(func.count(Article.id_article)).where(
        Article.language_code == language_code
    )
    result: Result = await session.execute(stmt)
    articles_count = result.scalar_one()
    return articles_count


async def get_article_by_language_code_and_position(
    session: AsyncSession,
    language_code: str,
    position: int,
) -> Article | None:
    """
    Get an article by language code and position in the database.
    """

    stmt = (
        select(Article)
        .where(Article.language_code == language_code)
        .order_by(Article.added_datetime.desc(), Article.id_article.desc())
        .offset(position - 1)
        .limit(1)
    )
    result: Result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    return article


async def get_article_by_id(session: AsyncSession, id_article: int) -> Article | None:
    """
    Get an article by ID.
    """

    stmt = select(Article).where(Article.id_article == id_article)
    result: Result = await session.execute(stmt)
    article = result.scalar_one_or_none()
    return article


async def delete_article(session: AsyncSession, article: Article) -> None:
    """
    Cancel an article.
    """

    await session.delete(article)
    await session.commit()
