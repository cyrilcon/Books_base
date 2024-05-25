from aiogram import Router

from .cancel_booking import cancel_booking_router
from .cancel_booking_cancel import cancel_booking_cancel_router

cancel_booking_routers = Router()
cancel_booking_routers.include_routers(
    cancel_booking_cancel_router,
    cancel_booking_router,
)
