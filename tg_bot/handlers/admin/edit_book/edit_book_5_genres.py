from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tg_bot.services import (
    ClearKeyboard,
    parse_and_format_genres,
    generate_book_caption,
    BookFormatter,
)
from tg_bot.states import EditBook

edit_genres_router = Router()


@edit_genres_router.callback_query(F.data.startswith("edit_genres"))
async def edit_genres(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    book = response.get_model()

    genres = BookFormatter.format_genres(book.genres)

    sent_message = await call.message.answer(
        l10n.format_value(
            "edit-book-prompt-genres",
            {"genres": f"<code>{genres}</code>"},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_genres)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_genres_router.message(StateFilter(EditBook.edit_genres), F.text)
async def edit_genres_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    genres_from_message = message.text

    genres, genre_too_long = await parse_and_format_genres(genres_from_message)
    if genre_too_long:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-genre-name-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.get_book_by_id(id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, genres=genres)
    caption_length = len(caption)

    if caption_length > 1024:
        sent_message = await message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.books.update_book(id_book_edited, genres=genres)
    book = response.get_model()

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
