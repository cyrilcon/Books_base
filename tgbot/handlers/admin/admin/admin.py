from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("admin"))
async def admin(message: Message, l10n: FluentLocalization):
    """
    Processing of the /start command.
    :param message: /start command.
    :param l10n: Config with bot parameters.
    :return: A message with commands for the administrator.
    """

    await message.answer(l10n.format_value("admin-commands"))
