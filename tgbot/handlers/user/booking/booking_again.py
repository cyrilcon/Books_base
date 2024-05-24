from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import (
    get_user_language,
)
from tgbot.states import Booking

booking_again_router = Router()


@booking_again_router.callback_query(F.data == "booking_again")
async def booking_again(call: CallbackQuery, state: FSMContext):
    """
    Повторный заказ книги.
    :param call: Нажатая кнопка "Заказать ещё".
    :param state: FSM (Booking).
    :return: Сообщение для написания названия книги и переход в FSM (send_title).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.answer(
        l10n.format_value("booking-title"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(Booking.send_title)
