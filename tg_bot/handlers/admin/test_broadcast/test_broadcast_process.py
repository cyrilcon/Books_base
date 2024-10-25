from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.services import Broadcaster
from tg_bot.states import TestBroadcast

test_broadcast_process_router = Router()


@test_broadcast_process_router.message(StateFilter(TestBroadcast.write_message))
async def test_broadcast_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    response = await api.users.admins.get_admin_ids()
    admin_ids = response.result

    await state.clear()
    success_count = await Broadcaster.broadcast(
        bot=bot,
        users=admin_ids,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await message.answer(
        l10n.format_value(
            "test-broadcast-success",
            {
                "success_count": success_count,
                "admin_ids": len(admin_ids),
            },
        )
    )
