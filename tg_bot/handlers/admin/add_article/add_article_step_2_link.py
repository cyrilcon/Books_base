import re

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
    languages_back_cancel_keyboard,
)
from tg_bot.states import AddArticle

add_article_step_2_router = Router()


@add_article_step_2_router.callback_query(
    StateFilter(AddArticle.add_link),
    F.data == "back",
)
async def back_to_add_article_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    title = data.get("title")

    await call.message.edit_text(
        l10n.format_value(
            "add-article-title-back",
            {"title": title},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddArticle.add_title)
    await call.answer()


@add_article_step_2_router.message(
    StateFilter(AddArticle.add_link),
    F.text,
)
async def add_article_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    link = message.text

    if len(link) > 255:
        await message.answer(
            l10n.format_value("add-article-error-link-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    if not re.match(r"^https://telegra\.ph/", link):
        await message.answer(
            l10n.format_value("add-article-error-invalid-link"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    response = await api.articles.get_article_by_link(link=link)
    status = response.status

    if status == 200:
        await message.answer(
            l10n.format_value("add-article-error-link-already-exists"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    await message.answer(
        l10n.format_value("add-article-language-code"),
        reply_markup=languages_back_cancel_keyboard(l10n),
    )
    await state.update_data(link=link)
    await state.set_state(AddArticle.select_language_code)
