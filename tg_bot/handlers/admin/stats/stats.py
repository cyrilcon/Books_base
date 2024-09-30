from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.services import ClearKeyboard

stats_router = Router()


@stats_router.message(Command("stats"))
async def stats(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    response = await api.users.get_user_statistics()
    statistic = response.get_model()

    await message.answer(
        l10n.format_value(
            "stats",
            {
                "active_last_hour": statistic.active_last_hour,
                "active_last_24_hours": statistic.active_last_24_hours,
                "active_last_week": statistic.active_last_week,
                "active_last_month": statistic.active_last_month,
                "total_users": statistic.total_users,
            },
        )
    )
    await state.clear()
