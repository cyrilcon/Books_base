import re

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tg_bot.services import BookFormatter
from tg_bot.states import AddBook

add_book_step_5_router = Router()


@add_book_step_5_router.callback_query(
    StateFilter(AddBook.add_genres),
    F.data == "back",
)
async def back_to_add_book_step_4(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    description = data.get("description")

    await call.message.edit_text(
        l10n.format_value(
            "add-book-description-back",
            {"description": description},
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_description)
    await call.answer()


@add_book_step_5_router.message(
    StateFilter(AddBook.add_genres),
    F.text,
)
async def add_book_step_5(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    genres_from_message = message.text

    data = await state.get_data()
    genres = data.get("genres")

    if genres is None:
        genres = []

    new_genres = [
        {"genre_name": genre}
        for genre in re.findall(r"\b(\w+(?:\s+\w+)*)\b", genres_from_message)
    ]

    for genre in new_genres:
        if len(genre["genre_name"]) > 255:
            await message.answer(
                l10n.format_value("add-book-error-genre-name-too-long"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            return

        if '"' in genre["genre_name"]:
            await message.answer(
                l10n.format_value("add-book-error-invalid-genre-name"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            return

        if genre["genre_name"] not in [g["genre_name"] for g in genres]:
            genres.append(genre)

    await state.update_data(genres=genres)

    genres = BookFormatter.format_genres(genres)
    await message.answer(
        l10n.format_value(
            "add-book-more-genres",
            {"genres": genres},
        ),
        reply_markup=done_clear_back_cancel_keyboard(l10n),
    )


@add_book_step_5_router.callback_query(
    StateFilter(AddBook.add_genres),
    F.data == "done",
)
async def add_book_step_5_done(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-cover"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_cover)
    await call.answer()


@add_book_step_5_router.callback_query(
    StateFilter(AddBook.add_genres),
    F.data == "clear",
)
async def add_book_5_clear(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("add-book-genres"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    genres = []
    await state.update_data(genres=genres)
    await call.answer()
