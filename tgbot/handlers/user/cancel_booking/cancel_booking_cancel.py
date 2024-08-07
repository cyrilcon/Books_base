from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import CancelBooking

cancel_booking_cancel_router = Router()
cancel_booking_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("cancel-booking-cancel")
)


@cancel_booking_cancel_router.callback_query(
    StateFilter(CancelBooking), F.data == "cancel"
)
async def cancel_booking_cancel():
    pass
