from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, is_book_article
from tgbot.states import AddBook

add_book_router_1 = Router()
add_book_router_1.message.filter(AdminFilter())


@add_book_router_1.message(Command("add_book"))
async def add_book_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    response = await api.books.get_latest_article()
    latest_article = response.result

    id_book = latest_article + 1
    free_article = "#{:04d}".format(id_book)

    sent_message = await message.answer(
        l10n.format_value(
            "add-book-article",
            {"free_article": free_article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.select_article)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_router_1.message(StateFilter(AddBook.select_article), F.text)
async def add_book_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    article = message.text

    response = await api.books.get_latest_article()
    latest_article = response.result

    id_book = latest_article + 1
    free_article = "#{:04d}".format(id_book)

    if is_book_article(article):
        id_book_from_message = int(article.lstrip("#"))

        response = await api.books.get_book_by_id(id_book_from_message)
        status = response.status

        if status == 200:
            sent_message = await message.answer(
                l10n.format_value(
                    "add-book-article-already-exists",
                    {"free_article": free_article},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
        else:
            sent_message = await message.answer(
                l10n.format_value("add-book-title"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            await state.update_data(id_book=id_book_from_message)
            await state.set_state(AddBook.add_title)
    else:
        sent_message = await message.answer(
            l10n.format_value(
                "add-book-article-incorrect",
                {"free_article": free_article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
