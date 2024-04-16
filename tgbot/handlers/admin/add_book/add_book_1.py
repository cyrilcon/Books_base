from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import cancel_button

add_book_router = Router()
add_book_router.message.filter(AdminFilter())


@add_book_router.message(Command("add_book"))
async def add_book_1(message: Message):
    """
    Обработка команды /add_book_1.
    :param message: Команда /add_book_1.
    :return: Сообщение для добавления артикула, вход в МС (AB1)
    """

    status, latest_article = await api.books.get_latest_article()
    latest_article = latest_article["latest_article"] + 1

    await message.answer(
        "<b>1/8</b>\n"
        "Введите <i><b>артикул</b></i> книги, чтобы добавить её в бд\n"
        f"Свободный артикул: <code>{'#{:04d}'.format(latest_article)}</code>",
        reply_markup=cancel_button,
    )
    # Вход в FSM
