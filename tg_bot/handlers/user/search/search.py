from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import search_by_keyboard

search_router = Router()


@search_router.message(Command("search"))
async def search(message: Message, l10n: FluentLocalization):
    await message.answer(
        l10n.format_value("search"),
        reply_markup=search_by_keyboard(l10n, by="title"),
    )
