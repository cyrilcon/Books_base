from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.services import get_user_language
from tgbot.states import Booking

booking_cancel_router = Router()


@booking_cancel_router.callback_query(StateFilter(Booking), F.data == "cancel")
async def booking_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена добавления заказа.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (Booking).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value("booking-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
