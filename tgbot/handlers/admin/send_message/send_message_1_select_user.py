from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard, back_and_cancel_keyboard
from tgbot.services import get_user_language, get_url_user, find_user
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

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    status, user, response_message = await find_user(message.text, l10n)

    if status == 200:
        id_user = user["id_user"]
        fullname = user["fullname"]
        username = user["username"]
        url_user = await get_url_user(fullname, username)

        await message.answer(
            l10n.format_value(
                "send-message-write-message",
                {"url_user": url_user, "id_user": str(id_user)},
            ),
            reply_markup=back_and_cancel_keyboard(l10n),
        )
        await state.update_data(id_user_recipient=id_user)
        await state.set_state(SendMessage.write_message)
    else:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
