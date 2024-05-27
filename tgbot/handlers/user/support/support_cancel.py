from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.services import get_user_language
from tgbot.states import Support

support_cancel_router = Router()


@support_cancel_router.callback_query(StateFilter(Support), F.data == "cancel")
async def support_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена отправки сообщения в тех-поддержку.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (Support).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    current_state = await state.get_state()

    if current_state.split(":")[-1] == "message_to_user":
        text = l10n.format_value("support-cancel-for-admin")
    else:
        text = l10n.format_value("support-cancel-for-user")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
