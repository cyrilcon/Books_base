from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import Booking

booking_again_router = Router()


@booking_again_router.callback_query(F.data == "booking_again")
async def booking_again(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)
    sent_message = await call.message.answer(
        l10n.format_value("booking-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Booking.send_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
