from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language, search_user
from tgbot.states import SendMessage

send_message_router_1 = Router()
send_message_router_1.message.filter(AdminFilter())


@send_message_router_1.message(Command("send_message"))
async def send_message_1(message: Message, state: FSMContext):
    """
    Обработка команды /send_message.
    :param message: Команда /send_message.
    :param state: FSM (SendMessage).
    :return: Сообщение для отправки сообщения пользователю и переход в FSM (SendMessage).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("send-message-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendMessage.select_user)


@send_message_router_1.message(StateFilter(SendMessage.select_user))
async def send_message_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Выбор пользователя для отправки сообщения.
    :param message: Сообщение с ожидаемым именем пользователя или его ID.
    :param bot: Экземпляр бота.
    :param state: FSM (SendMessage).
    :return: Сообщение для написания сообщения пользователю и переход в FSM (write_message).
    """

    text = "send-message-write-message"
    await search_user(message, bot, state, SendMessage.write_message, text)
