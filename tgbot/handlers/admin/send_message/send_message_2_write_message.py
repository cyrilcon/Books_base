from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    back_and_cancel_keyboard,
    cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tgbot.services import get_user_language, safe_send_message, send_message
from tgbot.states import SendMessage

send_message_router_2 = Router()
send_message_router_2.message.filter(AdminFilter())


@send_message_router_2.callback_query(
    StateFilter(SendMessage.write_message), F.data == "back"
)
async def back_to_send_message_1(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к выбору пользователя.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (SendMessage).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-message-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendMessage.select_recipient)


@send_message_router_2.message(StateFilter(SendMessage.write_message))
async def send_message_2(message: Message, bot: Bot, state: FSMContext, config: Config):
    """
    Отправка сообщения пользователю.
    :param message: Сообщение для отправки.
    :param bot: Экземпляр бота.
    :param state: FSM (SendMessage).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешной отправке сообщения.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    from_chat_id = message.from_user.id
    message_id = message.message_id

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    l10n_recipient = await get_user_language(id_user_recipient)

    is_sent = await safe_send_message(
        config=config,
        bot=bot,
        id_user=id_user_recipient,
        text=l10n_recipient.format_value("send-message-received"),
    )

    if is_sent:
        await send_message(config, bot, id_user_recipient, from_chat_id, message_id)
        await message.answer(l10n.format_value("send-message-sent"))
    else:
        await message.answer(l10n.format_value("user-blocked-bot"))

    await state.clear()
