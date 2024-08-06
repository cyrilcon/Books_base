from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import Booking

booking_cancel_router = Router()
booking_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("booking-cancel")
)


@booking_cancel_router.callback_query(StateFilter(Booking), F.data == "cancel")
async def booking_cancel():
    """
    Cancel adding an order.
    """

    pass
