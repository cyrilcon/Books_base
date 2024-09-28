from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import ClearKeyboard, generate_book_caption, BookFormatter
from tg_bot.states import EditBook
from .keyboards import edit_book_keyboard

edit_authors_router = Router()


@edit_authors_router.callback_query(F.data.startswith("edit_authors"))
async def edit_authors(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    authors = BookFormatter.format_authors(book.authors)

    sent_message = await call.message.answer(
        l10n.format_value(
            "edit-book-prompt-authors",
            {"authors": authors},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_authors)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_authors_router.message(
    StateFilter(EditBook.edit_authors),
    F.text,
)
async def edit_authors_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    authors = message.text.split(", ")

    for author_name in authors:
        if len(author_name) > 255:
            sent_message = await message.answer(
                l10n.format_value("edit-book-error-author-name-too-long"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                id_user=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
            return

        if '"' in author_name:
            sent_message = await message.answer(
                l10n.format_value("edit-book-error-invalid-author-name"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                id_user=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
            return

    authors = [{"author_name": author_name} for author_name in authors]

    data = await state.get_data()
    id_book_edited = data.get("id_edit_book")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, authors=authors)
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

    await api.books.update_book(id_book_edited=id_book_edited, authors=authors)

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
