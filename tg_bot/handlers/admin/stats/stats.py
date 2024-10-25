from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api

command_stats_router = Router()


@command_stats_router.message(Command("stats"))
async def stats(
    message: Message,
    l10n: FluentLocalization,
):
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
