from typing import Tuple, Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import view_news_keyboard
from tgbot.schemas import ArticleSchema

news_router = Router()


@news_router.message(Command("news"))
async def news(message: Message, l10n: FluentLocalization):
    articles_count, text, article, language_code = await get_article_info(
        l10n, id_user=message.from_user.id
    )

    if articles_count == 0:
        await message.answer(l10n.format_value("news-absent"))
    else:
        await message.answer(
            text=text,
            reply_markup=view_news_keyboard(
                l10n=l10n,
                articles_count=articles_count,
                language_code=language_code,
            ),
            link_preview_options=LinkPreviewOptions(
                url=article.link,
                prefer_large_media=True,
            ),
        )


@news_router.callback_query(F.data.startswith("article_page"))
async def article_position(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-1])

    articles_count, text, article, language_code = await get_article_info(
        l10n=l10n,
        id_user=call.from_user.id,
        position=page,
    )

    if articles_count == 0:
        await call.message.edit_text(l10n.format_value("news-absent"))
    else:
        await call.message.edit_text(
            text=text,
            reply_markup=view_news_keyboard(
                l10n=l10n,
                articles_count=articles_count,
                position=page,
                language_code=language_code,
            ),
            link_preview_options=LinkPreviewOptions(
                url=article.link,
                prefer_large_media=True,
            ),
        )
    await call.answer()


async def get_article_info(
    l10n: FluentLocalization,
    id_user: int,
    position: int = 1,
) -> Tuple[int, Optional[str], Optional[ArticleSchema], str]:
    """
    Retrieves article information and the total number of articles.

    First, it checks for articles in the user's language. If none are found,
    it checks the default language (Russian). If no articles are available,
    it returns 0 and no article data.

    :param l10n: User's localization for formatting the text.
    :param id_user: Unique user identifier.
    :param position: Article position in the database.
    :return: A tuple with the total number of articles, article text,
             ArticleSchema object, and language code.
    """

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()
    language_code = user.language_code

    response = await api.articles.get_articles_count_by_language_code(language_code)
    articles_count = response.result

    if articles_count == 0:
        language_code = "ru"
        response = await api.articles.get_articles_count_by_language_code(language_code)
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
            "link": article.link,
            "added-date": article.added_datetime,
        },
    )
    return articles_count, text, article, language_code
