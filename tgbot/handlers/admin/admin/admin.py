from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.filters import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin(message: Message):
    """
    Обработка команды /admin.
    :param message: Команда /admin.
    :return: Сообщение для админа.
    """

    await message.answer("Привет, админ!!")
