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
    orders_count, text, article = await get_article_info(
        l10n, id_user=message.from_user.id
    )

    if orders_count == 0:
        await message.answer(l10n.format_value("news-absent"))
    else:
        await message.answer(
            text=text,
            reply_markup=view_news_keyboard(l10n, orders_count),
            link_preview_options=LinkPreviewOptions(
                url=article.link,
                prefer_large_media=True,
            ),
        )


@news_router.callback_query(F.data.startswith("article_position"))
async def article_position(call: CallbackQuery, l10n: FluentLocalization):
    position = int(call.data.split(":")[-1])

    orders_count, text, article = await get_article_info(
        l10n=l10n,
        id_user=call.from_user.id,
        position=position,
    )

    if orders_count == 0:
        await call.message.edit_text(l10n.format_value("news-absent"))
    else:
        await call.message.edit_text(
            text=text,
            reply_markup=view_news_keyboard(
                l10n=l10n,
                orders_count=orders_count,
                position=position,
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
) -> Tuple[int, Optional[str], Optional[ArticleSchema]]:
    """
    Receive article information and total number of articles.

    :param l10n: Language set by the user.
    :param id_user: Unique user identifier.
    :param position: News position in the database.
    :return: A tuple containing the number of articles and text with order information.
    """

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()
    language_code = user.language_code

    response = await api.articles.get_articles_count_by_language_code(language_code)
    orders_count = response.result

    if orders_count == 0:
        response = await api.articles.get_articles_count_by_language_code("ru")
        orders_count = response.result

        if orders_count == 0:
            return orders_count, None, None

        return await get_article_info_success(position, l10n, orders_count)

    return await get_article_info_success(position, l10n, orders_count)


async def get_article_info_success(
    position: int,
    l10n: FluentLocalization,
    orders_count: int,
) -> Tuple[int, Optional[str], Optional[ArticleSchema]]:
    response = await api.articles.get_article_by_language_code_and_position(
        language_code="ru",
        position=position,
    )
    article = response.get_model()

    text = l10n.format_value(
        "article-template",
        {
            "title": article.title,
            "added-date": article.added_datetime,
        },
    )
    return orders_count, text, article
