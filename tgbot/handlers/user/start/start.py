from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message

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

    await message.answer("Привет, пользователь!!")
