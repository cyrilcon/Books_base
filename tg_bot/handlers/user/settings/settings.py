from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import languages_keyboard

command_settings_router = Router()


@command_settings_router.message(
    Command("settings"),
    flags={"safe_message": False},
)
async def settings(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(
        l10n.format_value("settings"),
        reply_markup=languages_keyboard(l10n),
    )
