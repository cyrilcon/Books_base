from aiogram import Router

from .booking import booking_routers
from .cancel_booking import cancel_booking_routers
from .privacy import privacy_router
from .settings import settings_router
from .share_base import share_base_routers
from .start import start_router
from .support import support_routers

user_routers = Router()
user_routers.include_routers(
    start_router,  # Must be the first
    booking_routers,
    cancel_booking_routers,
    privacy_router,
    settings_router,
    share_base_routers,
    support_routers,
    # search_routers,  # Must be the latest
)
