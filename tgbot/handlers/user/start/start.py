from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.states import all_states

start_router = Router()


@start_router.message(CommandStart())
@start_router.message(StateFilter(all_states))
async def start(message: Message):
    """
    Обработка команды /start.
    :param message: Команда /start.
    :return: Сообщение приветствие бота.
    """

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    status, result = await api.get_user(id_user)
    if status == 404:
        await api.add_user(id_user, fullname, username)

    text = f", <b>{fullname}</b>" if fullname else None
    await message.answer(
        f"Привет{text}!!\n"
        "Напиши название или артикул книги, чтобы купить и ознакомится с товаром"
    )
