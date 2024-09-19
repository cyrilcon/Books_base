from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import ClearKeyboard, Broadcaster
from tg_bot.states import Broadcast

broadcast_router = Router()


@broadcast_router.message(Command("broadcast"))
async def broadcast(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("broadcast-prompt-write-message"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Broadcast.write_message)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@broadcast_router.message(StateFilter(Broadcast.write_message), F.text)
async def broadcast_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    response = await api.users.get_user_ids()
    users = response.result

    from_chat_id = message.chat.id
    message_id = message.message_id

    await state.clear()
    success_count = await Broadcaster.broadcast(bot, users, from_chat_id, message_id)

    await message.answer(
        l10n.format_value(
            "broadcast-success",
            {"success_count": success_count, "users_count": len(users)},
        )
    )
