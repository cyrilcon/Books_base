from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
    back_yes_cancel_keyboard,
)
from tg_bot.services import BookFormatter
from tg_bot.states import AddBook

add_book_step_2_router = Router()


@add_book_step_2_router.callback_query(
    StateFilter(AddBook.add_title),
    F.data == "back",
)
async def back_to_add_book_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    free_article = data.get("free_article")

    await call.message.edit_text(
        l10n.format_value(
            "add-book-article",
            {"free_article": free_article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.select_article)
    await call.answer()


@add_book_step_2_router.message(
    StateFilter(AddBook.add_title),
    F.text,
)
async def add_book_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    title = message.text

    if len(title) > 255:
        await message.answer(
            l10n.format_value("add-book-error-title-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    if '"' in title:
        await message.answer(
            l10n.format_value("add-book-error-invalid-title"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    response = await api.books.search_books_by_title(
        title=title,
        similarity_threshold=100,
    )
    result = response.get_model()

    if result.found > 0:
        book = result.books[0].book
        article = BookFormatter.format_article(book.id_book)

        await message.answer(
            l10n.format_value(
                "add-book-error-title-already-exists",
                {
                    "title": book.title,
                    "article": article,
                },
            ),
            reply_markup=back_yes_cancel_keyboard(l10n),
        )
        return

    await message.answer(
        l10n.format_value("add-book-authors"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(title=title)
    await state.set_state(AddBook.add_authors)


@add_book_step_2_router.callback_query(
    StateFilter(AddBook.add_title),
    F.data == "yes",
)
async def add_book_step_2_yes(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-authors"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)
    await call.answer()
