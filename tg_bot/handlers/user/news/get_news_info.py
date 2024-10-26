from typing import Tuple, Optional

from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from api.api_v1.schemas import ArticleSchema, UserSchema


async def get_article_info(
    l10n: FluentLocalization,
    user: UserSchema,
    position: int = 1,
) -> Tuple[int, Optional[str], Optional[ArticleSchema], str]:
    """
    Retrieves article information and the total number of articles.

    First, it checks for articles in the user's language. If none are found,
    it checks the default language (Russian). If no articles are available,
    it returns 0 and no article data.

    :param l10n: User's localization for formatting the text.
    :param user: User instance.
    :param position: Article position in the database.
    :return: A tuple with the total number of articles, article text,
             ArticleSchema object, and language code.
    """

    language_code = user.language_code

    response = await api.articles.get_articles_count_by_language_code(
        language_code=language_code
    )
    articles_count = response.result

    if articles_count == 0:
        language_code = "ru"
        response = await api.articles.get_articles_count_by_language_code(
            language_code=language_code
        )
        articles_count = response.result

        if articles_count == 0:
            return articles_count, None, None, language_code

        return await get_article_info_success(
            language_code, position, l10n, articles_count
        )

    return await get_article_info_success(language_code, position, l10n, articles_count)


async def get_article_info_success(
    language_code: str,
    position: int,
    l10n: FluentLocalization,
    articles_count: int,
) -> Tuple[int, Optional[str], Optional[ArticleSchema], str]:
    """
    Retrieves a specific article based on language and page number.

    :param language_code: Language code for fetching the article.
    :param position: Article position in the database.
    :param l10n: Localization object for formatting text.
    :param articles_count: Total number of articles for the language.
    :return: A tuple with the total number of articles, formatted article text,
             ArticleSchema object, and language code.
    """

    response = await api.articles.get_article_by_language_code_and_position(
        language_code=language_code,
        position=position,
    )
    article = response.get_model()

    text = l10n.format_value(
        "article-template",
        {
            "title": article.title,
            "link": str(article.main_link),
            "added-date": article.added_datetime,
        },
    )
    return articles_count, text, article, language_code
