from aiogram import Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.services.messaging import Broadcaster
from tg_bot.states import Broadcast

broadcast_process_router = Router()


@broadcast_process_router.message(StateFilter(Broadcast.write_message))
async def broadcast_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    response = await api.users.get_user_ids()
    user_ids = response.result

    response = await api.users.blacklist.get_blacklisted_user_ids()
    blacklisted_user_ids = response.result

    await state.clear()
    success_count = await Broadcaster.broadcast(
        bot=bot,
        users=list(set(user_ids) - set(blacklisted_user_ids)),
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await message.answer(
        l10n.format_value(
            "broadcast-success",
            {
                "success_count": success_count,
                "users_count": len(user_ids),
                "blacklisted_users_count": len(blacklisted_user_ids),
            },
        )
    )
