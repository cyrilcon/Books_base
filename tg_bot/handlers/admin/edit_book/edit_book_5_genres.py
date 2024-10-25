import re

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tg_bot.services import generate_book_caption, BookFormatter
from tg_bot.states import EditBook

edit_genres_router = Router()


@edit_genres_router.callback_query(
    F.data.startswith("edit_genres"),
    flags={"skip_message": 1},
)
async def edit_genres(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    genres = BookFormatter.format_genres(book.genres)

    await call.message.answer(
        l10n.format_value(
            "edit-book-genres",
            {"genres": genres},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_genres)
    await call.answer()


@edit_genres_router.message(
    StateFilter(EditBook.edit_genres),
    F.text,
)
async def edit_genres_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    genres_from_message = message.text

    genres = []

    new_genres = re.findall(r"\b(\w+(?:\s+\w+)*)\b", genres_from_message)
    new_genres = [{"genre_name": genre} for genre in new_genres]

    for genre in new_genres:
        if len(genre["genre_name"]) > 255:
            await message.answer(
                l10n.format_value("edit-book-error-genre-name-too-long"),
                reply_markup=cancel_keyboard(l10n),
            )
            return

        if '"' in genre["genre_name"]:
            await message.answer(
                l10n.format_value("add-book-error-invalid-genre-name"),
                reply_markup=cancel_keyboard(l10n),
            )
            return

        if genre["genre_name"] not in [g["genre_name"] for g in genres]:
            genres.append(genre)

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, genres=genres)
    caption_length = len(caption)

    if caption_length > 1024:
        await message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    response = await api.books.update_book(id_book_edited=id_book_edited, genres=genres)
    book = response.get_model()

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=book.id_book),
    )
    await state.clear()
