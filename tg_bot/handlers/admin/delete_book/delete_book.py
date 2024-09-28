from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import ClearKeyboard, is_valid_book_article
from tg_bot.states import DeleteBook

delete_book_router = Router()


@delete_book_router.message(Command("delete_book"))
async def delete_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("delete-book-prompt-select-book"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(DeleteBook.select_book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@delete_book_router.message(
    StateFilter(DeleteBook.select_book),
    F.text,
)
async def delete_book_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    if not is_valid_book_article(article):
        sent_message = await message.answer(
            l10n.format_value("delete-book-error-invalid-article"),
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
            l10n.format_value("delete-book-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    book = response.get_model()
    await api.books.delete_book(id_book=id_book)

    await message.answer(
        l10n.format_value(
            "delete-book-success",
            {"title": book.title},
        )
    )
    await state.clear()
