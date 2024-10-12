from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from tg_bot.middlewares import SaturdayMiddleware
from tg_bot.services import saturday_post

command_saturday_post_router = Router()
command_saturday_post_router.message.middleware(SaturdayMiddleware())


@command_saturday_post_router.message(Command("saturday_post"))
async def saturday_post_handler(message: Message, bot: Bot):
    await saturday_post(bot)
