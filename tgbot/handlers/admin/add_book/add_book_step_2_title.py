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
    back_yes_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, BookFormatter
from tgbot.states import AddBook

add_book_step_2_router = Router()


@add_book_step_2_router.callback_query(StateFilter(AddBook.add_title), F.data == "back")
async def back_to_add_book_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    response = await api.books.get_latest_article()
    latest_article = response.result
    free_article = BookFormatter.format_article(latest_article + 1)

    await call.message.edit_text(
        l10n.format_value(
            "add-book-prompt-article",
            {"free_article": free_article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.select_article)
    await call.answer()


@add_book_step_2_router.message(StateFilter(AddBook.add_title), F.text)
async def add_book_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    title = message.text

    if len(title) > 255:
        sent_message = await message.answer(
            l10n.format_value("add-book-error-title-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    if '"' in title:
        sent_message = await message.answer(
            l10n.format_value("add-book-error-invalid-title"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.books.search_books_by_title(title, similarity_threshold=100)
    result = response.get_model()

    if result.found > 0:
        book = result.books[0].book
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-error-title-already-exists",
                {
                    "title": book.title,
                    "article": BookFormatter.format_article(book.id_book),
                },
            ),
            reply_markup=back_yes_cancel_keyboard(l10n),
        )
    else:
        sent_message = await message.answer(
            l10n.format_value("add-book-prompt-authors"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await state.set_state(AddBook.add_authors)

    await state.update_data(title=title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_step_2_router.callback_query(StateFilter(AddBook.add_title), F.data == "yes")
async def add_book_step_2_yes(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-prompt-authors"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)
    await call.answer()
