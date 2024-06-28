from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import Config
from tgbot.keyboards.inline import (
    cancel_keyboard,
    support_answer_keyboard,
)
from tgbot.services import (
    get_user_language,
    safe_send_message,
)
from tgbot.states import Support

support_reply_to_user_router = Router()


@support_reply_to_user_router.callback_query(F.data.startswith("support_answer"))
async def support_reply_to_user(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопки "Ответить".
    :param call: Кнопка "Ответить".
    :param state: FSM (Support).
    :return: Сообщение для отправки сообщения пользователю и переход в FSM (message_to_user).
    """

    id_admin = call.from_user.id
    l10n = await get_user_language(id_admin)

    id_user = call.data.split(":")[-1]
    await state.update_data(id_user=id_user)

    await call.answer(cache_time=1)
    await call.message.answer(
        l10n.format_value("support-preparation-report"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Support.message_to_user)


@support_reply_to_user_router.message(StateFilter(Support.message_to_user))
async def support_reply_to_user_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Отправка ответа пользователю.
    :param message: Сообщение с ожидаемым сообщением дял пользователя.
    :param bot: Экземпляр бота.
    :param state: FSM (Support).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешной отправке сообщения пользователю.
    """

    data = await state.get_data()
    id_user = data["id_user"]
    l10n = await get_user_language(id_user)

    reply = message.html_text

    is_sent = await safe_send_message(
        config=config,
        bot=bot,
        id_user=id_user,
        text=l10n.format_value("support-message-from-admin", {"reply": reply}),
        reply_markup=support_answer_keyboard(l10n),
    )
    if is_sent:
        await message.answer(l10n.format_value("support-message-sent-to-user"))
    else:
        await message.answer(l10n.format_value("support-message-user-blocked-bot"))
    await state.clear()
