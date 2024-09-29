from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.services import ClearKeyboard

start_router = Router()


@start_router.message(CommandStart())
async def start(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    full_name = message.from_user.full_name
    await message.answer(l10n.format_value("start", {"full_name": full_name}))
