__all__ = (
    "user_commands_router",
    "user_routers",
)

from aiogram import Router

from tg_bot.middlewares import ResetStateMiddleware
from .start import start_routers

from .booking import booking_router

user_commands_router = Router()
user_commands_router.message.middleware(ResetStateMiddleware())
user_commands_router.include_routers(
    start_routers,  # Must be the first
)

user_routers = Router()
user_routers.include_routers(
    booking_router,
    # search_routers,  # Must be the latest
)
