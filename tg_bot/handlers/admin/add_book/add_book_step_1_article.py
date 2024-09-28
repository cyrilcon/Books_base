from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import ClearKeyboard, is_valid_book_article, BookFormatter
from tg_bot.states import AddBook

add_book_step_1_router = Router()


@add_book_step_1_router.message(Command("add_book"))
async def add_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    response = await api.books.get_latest_article()
    latest_article = response.result

    id_book = latest_article + 1
    free_article = BookFormatter.format_article(id_book)

    sent_message = await message.answer(
        l10n.format_value(
            "add-book-prompt-article",
            {"free_article": free_article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(free_article=free_article)
    await state.set_state(AddBook.select_article)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_step_1_router.message(
    StateFilter(AddBook.select_article),
    F.text,
)
async def add_book_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    data = await state.get_data()
    free_article = data.get("free_article")

    if not is_valid_book_article(article):
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-error-invalid-article",
                {"free_article": free_article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status == 200:
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-error-article-already-exists",
                {"free_article": free_article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        sent_message = await message.answer(
            l10n.format_value("add-book-prompt-title"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await state.update_data(id_book=id_book)
        await state.set_state(AddBook.add_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
