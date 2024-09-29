from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import (
    ClearKeyboard,
    is_valid_book_article,
    generate_book_caption,
    BookFormatter,
)
from tg_bot.states import EditBook
from .keyboards import edit_book_keyboard

edit_article_router = Router()


@edit_article_router.callback_query(F.data.startswith("edit_article"))
async def edit_article(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.message.edit_reply_markup()

    id_book = int(call.data.split(":")[-1])
    article = BookFormatter.format_article(id_book)

    sent_message = await call.message.answer(
        l10n.format_value(
            "edit-book-article",
            {"article": article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_article)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@edit_article_router.message(
    StateFilter(EditBook.edit_article),
    F.text,
)
async def edit_article_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if not is_valid_book_article(article):
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    new_id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=new_id_book)
    status = response.status

    if status == 200:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-article-already-exists"),
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

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        id_book=new_id_book,
    )
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

    response = await api.books.update_book(
        id_book_edited=id_book_edited,
        id_book=new_id_book,
    )
    book = response.get_model()

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, book.id_book),
    )
    await state.clear()
