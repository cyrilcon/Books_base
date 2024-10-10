from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluent.runtime import FluentLocalization

command_start_router = Router()


@command_start_router.message(CommandStart())
async def start(
    message: Message,
    l10n: FluentLocalization,
):
    full_name = message.from_user.full_name
    await message.answer(
        l10n.format_value(
            "start",
            {"full_name": full_name},
        )
    )
