from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from config import config
from api.api_v1.schemas import UserSchema
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.services import set_user_commands

command_start_router = Router()


@command_start_router.message(
    CommandStart(),
    flags={"safe_message": False},
)
async def start(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
    user: UserSchema,
):
    await message.answer(
        l10n.format_value(
            "start",
            {
                "full_name": user.full_name,
                "channel_link": config.channel.link,
            },
        ),
        reply_markup=channel_keyboard(l10n),
    )
    await set_user_commands(
        bot=bot,
        id_user=user.id_user,
        is_admin=True if user.is_admin else False,
    )
