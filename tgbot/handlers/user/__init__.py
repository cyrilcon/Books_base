from aiogram import Router

from .booking import booking_routers
from .cancel_booking import cancel_booking_routers
from .search import search_routers
from .start import start_router

user_routers = Router()
user_routers.include_routers(
    start_router,
    booking_routers,
    cancel_booking_routers,
    search_routers,
)
