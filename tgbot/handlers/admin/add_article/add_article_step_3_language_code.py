from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import back_cancel_keyboard
from tgbot.states import AddArticle

add_article_step_3_router = Router()


@add_article_step_3_router.callback_query(
    StateFilter(AddArticle.select_language_code), F.data == "back"
)
async def back_to_add_article_step_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-article-prompt-link"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddArticle.add_link)
    await call.answer()


@add_article_step_3_router.callback_query(
    StateFilter(AddArticle.select_language_code),
    F.data.startswith("language"),
)
async def add_article_step_3(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    language_code = call.data.split(":")[-1]

    data = await state.get_data()
    link = data.get("link")
    title = data.get("title")

    response = await api.articles.create_article(link, title, language_code)
    article = response.get_model()

    title = article.title
    added_date = article.added_datetime

    await call.message.edit_text(
        l10n.format_value(
            "add-article-success",
            {
                "title": title,
                "added-date": added_date,
            },
        ),
        link_preview_options=LinkPreviewOptions(
            url=article.link,
            prefer_large_media=True,
        ),
    )
    await state.clear()
    await call.answer()
