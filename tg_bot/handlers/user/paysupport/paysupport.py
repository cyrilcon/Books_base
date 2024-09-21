from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

paysupport_router = Router()


@paysupport_router.message(Command("paysupport"))
async def paysupport(message: Message, l10n: FluentLocalization):
    await message.answer(l10n.format_value("paysupport"))
