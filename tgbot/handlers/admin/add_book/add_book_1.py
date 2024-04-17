import re

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_button, back_and_cancel_buttons
from tgbot.services import get_fluent_localization
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

    language = message.from_user.language_code
    l10n = get_fluent_localization(language)

    status, latest_article = await api.books.get_latest_article()
    free_article = "#{:04d}".format(latest_article["latest_article"] + 1)

    await message.answer(
        l10n.format_value("add-book-article", {"free_article": free_article}),
        reply_markup=cancel_button,
    )

    await state.set_state(AddBook.select_article)  # Вход в FSM (select_article)


@add_book_router_1.message(StateFilter(AddBook.select_article))
async def add_book_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор артикула для книги.
    :param message: Сообщение с ожидаемым артикулом книги.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления названия книги и переход в FSM (add_name_book).
    """

    await delete_keyboard(bot, message)  # Удаляются inline кнопки

    id_user = message.from_user.id
    status, user = await api.users.get_user(id_user)

    language = user["language"]
    l10n = get_fluent_localization(language)

    article = message.text  # Артикул добавляемой книги

    status, latest_article = await api.books.get_latest_article()
    free_article = "#{:04d}".format(latest_article["latest_article"] + 1)

    # Проверка формата артикула
    if not article.startswith("#") or not re.fullmatch(r"#\d{4}", article):
        await message.answer(
            l10n.format_value(
                "add-book-incorrect-article",
                {"free_article": free_article},
            ),
            reply_markup=cancel_button,
        )
    else:
        id_book = int(article.strip("#"))  # id книги (без символа "#")

        status, book = await api.books.get_book(id_book)

        if status == 200:
            await message.answer(
                l10n.format_value(
                    "add-book-article-already-exist",
                    {"free_article": free_article},
                ),
                reply_markup=cancel_button,
            )
        else:
            await state.update_data(article=article)  # Сохраняется артикул
            await message.answer(
                l10n.format_value("add-book-name-book"),
                reply_markup=back_and_cancel_buttons,
            )
            await state.set_state(AddBook.add_name_book)  # Вход в FSM (add_name_book)
