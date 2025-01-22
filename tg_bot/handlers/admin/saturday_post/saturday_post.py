from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.middlewares import SaturdayMiddleware
from tg_bot.services.specials import saturday_post

command_saturday_post_router = Router()
command_saturday_post_router.message.middleware(SaturdayMiddleware())


@command_saturday_post_router.message(Command("saturday_post"))
async def saturday_post_handler(
    message: Message,
    l10n: FluentLocalization,
    bot: Bot,
):
    await saturday_post(bot)
    await message.answer(l10n.format_value("saturday-post-success"))
