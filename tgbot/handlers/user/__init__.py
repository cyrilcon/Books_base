from aiogram import Router

from .base_store import base_store_routers
from .booking import booking_routers
from .cancel_booking import cancel_booking_routers
from .search import search_routers
from .start import start_router
from .support import support_routers

user_routers = Router()
user_routers.include_routers(
    start_router,
    base_store_routers,
    booking_routers,
    cancel_booking_routers,
    support_routers,
    search_routers,
)
