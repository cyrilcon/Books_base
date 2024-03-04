from aiogram import Router
from aiogram import types, F
from aiogram.filters import StateFilter

from tgbot.filters.private_chat import IsPrivate

echo_router = Router()
echo_router.message.filter(IsPrivate())


@echo_router.message(F.text, StateFilter(None))
async def echo(message: types.Message):
    """
    Обработка необработанных сообщений.
    :param message: Любое необработанное сообщение.
    """

    await message.answer("Мы вас не поняли 😕\n"
                         "Список команд – /help")
