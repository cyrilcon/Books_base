from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

privacy_router = Router()


@privacy_router.message(Command("privacy"))
async def privacy(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("privacy"))
