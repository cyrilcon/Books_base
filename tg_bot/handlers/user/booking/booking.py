from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.services import ClearKeyboard

booking_router = Router()


@booking_router.message(Command("booking"))
async def booking(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    await message.answer(l10n.format_value("booking"))
