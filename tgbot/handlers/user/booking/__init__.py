from aiogram import Router

from .booking_1_title import booking_router_1
from .booking_2_author import booking_router_2
from .booking_again import booking_again_router
from .booking_cancel import booking_cancel_router

booking_routers = Router()
booking_routers.include_routers(
    booking_cancel_router,
    booking_router_1,
    booking_router_2,
    booking_again_router,
)
