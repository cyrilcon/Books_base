from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.enums import SearchBy
from .keyboards import search_by_keyboard

command_search_router = Router()


@command_search_router.message(
    Command("search"),
    flags={"safe_message": False},
)
async def search(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(
        l10n.format_value("search"),
        reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
    )
