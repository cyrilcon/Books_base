from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from api.books_base_api.schemas import UserSchema
from tg_bot.handlers.user.news.get_news_info import get_article_info
from tg_bot.keyboards.inline import view_articles_keyboard

command_news_router = Router()


@command_news_router.message(
    Command("news"),
    flags={"safe_message": False},
)
async def news(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
):
    articles_count, text, article, language_code = await get_article_info(
        l10n=l10n,
        user=user,
    )

    if articles_count == 0:
        await message.answer(l10n.format_value("news-absent"))
    else:
        await message.answer(
            text=text,
            reply_markup=view_articles_keyboard(
                l10n=l10n,
                articles_count=articles_count,
                language_code=language_code,
            ),
            link_preview_options=LinkPreviewOptions(
                url=str(article.link),
                prefer_large_media=True,
            ),
        )
