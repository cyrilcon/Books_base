from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

command_help_router = Router()


@command_help_router.message(Command("help"))
async def help(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("help"))
