import re

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard

from tgbot.services import get_user_language
from tgbot.states import DeleteBook

delete_book_router = Router()
delete_book_router.message.filter(AdminFilter())


@delete_book_router.message(Command("delete_book"))
async def delete_book(message: Message, state: FSMContext):
    """
    Обработка команды /delete_book.
    :param message: Команда /delete_book.
    :param state: FSM (DeleteBook).
    :return: Сообщение для ввода артикула и переход в FSM (delete_book).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("delete-book"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(DeleteBook.delete_book)


@delete_book_router.message(StateFilter(DeleteBook.delete_book))
async def delete_book_process(message: Message, bot: Bot, state: FSMContext):
    """
    Удаление книги.
    :param message: Сообщение с ожидаемым артикулом книги.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления названия книги и переход в FSM (add_name_book).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    article = message.text

    if not article.startswith("#") or not re.fullmatch(r"#\d{4}", article):
        await message.answer(
            l10n.format_value("delete-book-article-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        id_book = int(article[1:])

        response = await api.books.get_book(id_book)
        status = response.status
        book = response.result

        if status == 200:
            await api.books.delete_book(id_book)

            await message.answer(
                l10n.format_value(
                    "delete-book-successful-deleted",
                    {
                        "title": book["title"],
                        "id_book": "#{:04d}".format(book["id_book"]),
                    },
                )
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value("delete-book-not-found"),
                reply_markup=cancel_keyboard(l10n),
            )
