from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import get_user_language, ClearKeyboard, Messenger, Broadcaster
from tgbot.states import SendMessage

send_message_router_2 = Router()
send_message_router_2.message.filter(AdminFilter())


@send_message_router_2.callback_query(
    StateFilter(SendMessage.write_message), F.data == "back"
)
async def back_to_send_message_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-message-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendMessage.select_user)


@send_message_router_2.message(StateFilter(SendMessage.write_message))
async def send_message_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    from_chat_id = message.from_user.id
    message_id = message.message_id

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    l10n_recipient = await get_user_language(id_user_recipient)

    is_sent = await Messenger.safe_send_message(
        bot=bot,
        user_id=id_user_recipient,
        text=l10n_recipient.format_value("send-message-received"),
    )

    if is_sent:
        await Broadcaster.send_message(
            bot=bot,
            chat_id=id_user_recipient,
            from_chat_id=from_chat_id,
            message_id=message_id,
        )
        await message.answer(l10n.format_value("send-message-success"))
    else:
        await message.answer(l10n.format_value("user-blocked-bot"))

    await state.clear()
