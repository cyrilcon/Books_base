from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.services import get_user_language
from tgbot.states import CancelBooking

cancel_booking_cancel_router = Router()
cancel_booking_cancel_router.message.filter(AdminFilter())


@cancel_booking_cancel_router.callback_query(
    StateFilter(CancelBooking), F.data == "cancel"
)
async def cancel_booking_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена отмены заказа.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (CancelBooking).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value("cancel-booking-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
