import re

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_and_cancel_keyboard,
)
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_1 = Router()
add_book_router_1.message.filter(AdminFilter())


@add_book_router_1.message(Command("add_book"))
async def add_book_1(message: Message, state: FSMContext):
    """
    Обработка команды /add_book_1.
    :param message: Команда /add_book_1.
    :param state: FSM (AddBook).
    :return: Сообщение для выбора артикула и переход в FSM (select_article).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    response = await api.books.get_latest_article()
    latest_article = response.result

    id_book = latest_article + 1
    free_article = "#{:04d}".format(id_book)

    await message.answer(
        l10n.format_value("add-book-article", {"free_article": free_article}),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(AddBook.select_article)


@add_book_router_1.message(StateFilter(AddBook.select_article))
async def add_book_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор артикула для книги.
    :param message: Сообщение с ожидаемым артикулом книги.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления названия книги и переход в FSM (add_name_book).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    article = message.text

    response = await api.books.get_latest_article()
    latest_article = response.result

    id_book = latest_article + 1
    free_article = "#{:04d}".format(id_book)

    if not article.startswith("#") or not re.fullmatch(r"#\d{4}", article):
        await message.answer(
            l10n.format_value(
                "add-book-incorrect-article",
                {"free_article": free_article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        response = await api.books.get_book(id_book)
        status = response.status

        if status == 200:
            await message.answer(
                l10n.format_value(
                    "add-book-article-already-exist",
                    {"free_article": free_article},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
        else:
            await message.answer(
                l10n.format_value("add-book-title"),
                reply_markup=back_and_cancel_keyboard(l10n),
            )
            await state.update_data(id_book=id_book)
            await state.set_state(AddBook.add_title)
