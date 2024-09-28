from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import ClearKeyboard, is_valid_book_article, generate_book_caption
from tg_bot.states import EditBook
from .keyboards import edit_book_keyboard

edit_book_router = Router()


@edit_book_router.message(Command("edit_book"))
async def edit_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("edit-book-prompt-select-book"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(EditBook.select_book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@edit_book_router.message(
    StateFilter(EditBook.select_book),
    F.text,
)
async def edit_book_process(
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

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("edit-book-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    book = response.get_model()
    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=id_book),
    )
    await state.clear()
