from aiogram import Router

from .base_store import base_store_routers
from .booking import booking_router
from .cancel_order import cancel_order_routers
from .order import order_routers
from .privacy import privacy_router
from .search import search_routers
from .settings import settings_router
from .share_base import share_base_routers
from .start import start_router
from .support import support_routers

user_routers = Router()
user_routers.include_routers(
    start_router,  # Must be the first
    base_store_routers,
    booking_router,
    cancel_order_routers,
    order_routers,
    privacy_router,
    settings_router,
    share_base_routers,
    support_routers,
    search_routers,  # Must be the latest
)
