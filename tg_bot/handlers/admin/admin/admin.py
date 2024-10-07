from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

command_admin_router = Router()


@command_admin_router.message(Command("admin"))
async def admin(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("admin"))
