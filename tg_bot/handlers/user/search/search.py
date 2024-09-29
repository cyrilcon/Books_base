from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.enums import SearchBy
from tg_bot.services import ClearKeyboard
from .keyboards import search_by_keyboard

search_router = Router()


@search_router.message(Command("search"))
async def search(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    await message.answer(
        l10n.format_value("search"),
        reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
    )
