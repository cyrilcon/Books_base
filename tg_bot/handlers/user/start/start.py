from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api.schemas import UserSchema
from tg_bot.services import set_user_commands

command_start_router = Router()


@command_start_router.message(CommandStart())
async def start(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
    user: UserSchema,
):
    await message.answer(
        l10n.format_value(
            "start",
            {"full_name": user.full_name},
        )
    )
    await set_user_commands(
        bot=bot,
        id_user=user.id_user,
        is_admin=True if user.is_admin else False,
    )
