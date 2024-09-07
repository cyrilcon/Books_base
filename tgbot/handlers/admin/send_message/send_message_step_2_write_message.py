from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import cancel_keyboard, reply_keyboard
from tgbot.services import ClearKeyboard, get_user_language
from tgbot.states import SendMessage

send_message_router_2_router = Router()


@send_message_router_2_router.callback_query(
    StateFilter(SendMessage.write_message), F.data == "back"
)
async def back_to_send_message_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("send-message-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendMessage.select_user)
    await call.answer()


@send_message_router_2_router.message(StateFilter(SendMessage.write_message))
async def support_reply_to_user_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    data = await state.get_data()
    id_user_recipient = data["id_user_recipient"]
    user_link = data["user_link"]

    l10n_recipient = await get_user_language(id_user_recipient)

    try:
        sent_message = await bot.copy_message(
            chat_id=id_user_recipient,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
        )
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value("send-message-from-admin"),
            reply_markup=reply_keyboard(l10n),
            reply_to_message_id=sent_message.message_id,
        )
    except AiogramError:
        await message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await message.answer(
            l10n.format_value(
                "send-message-success",
                {
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                },
            )
        )
    await state.clear()
