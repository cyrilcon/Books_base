import re

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
    languages_back_cancel_keyboard,
)
from tgbot.services import ClearKeyboard
from tgbot.states import AddArticle

add_article_step_2_router = Router()


@add_article_step_2_router.callback_query(
    StateFilter(AddArticle.add_link), F.data == "back"
)
async def back_to_add_article_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-article-prompt-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddArticle.add_title)
    await call.answer()


@add_article_step_2_router.message(StateFilter(AddArticle.add_link), F.text)
async def add_article_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    link = message.text

    if len(link) > 255:
        sent_message = await message.answer(
            l10n.format_value("add-article-error-link-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    if not re.match(r"^(https://)?telegra\.ph/", link):
        sent_message = await message.answer(
            l10n.format_value("add-article-error-invalid-link"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.articles.get_article_by_link(link)
    status = response.status

    if status == 200:
        sent_message = await message.answer(
            l10n.format_value("add-article-error-link-already-exists"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    sent_message = await message.answer(
        l10n.format_value("add-article-prompt-language-code"),
        reply_markup=languages_back_cancel_keyboard(l10n),
    )
    await state.update_data(link=link)
    await state.set_state(AddArticle.select_language_code)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
