from aiogram import Router, F
from aiogram.types import CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from tg_bot.api_client.schemas import UserSchema
from tg_bot.handlers.user.news.get_news_info import get_article_info
from tg_bot.keyboards.inline import view_articles_keyboard

news_position_router = Router()


@news_position_router.callback_query(
    F.data.startswith("article_position"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def article_position(
    call: CallbackQuery,
    l10n: FluentLocalization,
    user: UserSchema,
):
    page = int(call.data.split(":")[-1])

    articles_count, text, article, language_code = await get_article_info(
        l10n=l10n,
        user=user,
        position=page,
    )

    if articles_count == 0:
        await call.message.edit_text(l10n.format_value("news-absent"))
    else:
        await call.message.edit_text(
            text=text,
            reply_markup=view_articles_keyboard(
                l10n=l10n,
                articles_count=articles_count,
                position=page,
                language_code=language_code,
            ),
            link_preview_options=LinkPreviewOptions(
                url=str(article.link),
                prefer_large_media=True,
            ),
        )
    await call.answer()
