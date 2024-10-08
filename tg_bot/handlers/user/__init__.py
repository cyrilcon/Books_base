__all__ = (
    "user_commands_router",
    "user_routers",
)

from aiogram import Router

from tg_bot.middlewares import ResetStateMiddleware
from .booking import command_booking_router
from .my_books import command_my_books_router, my_books_routers
from .paysupport import command_paysupport_router
from .privacy import command_privacy_router
from .settings import command_settings_router, settings_routers
from .start import start_routers

user_commands_router = Router()
user_commands_router.message.middleware(ResetStateMiddleware())
user_commands_router.include_routers(
    start_routers,  # Must be the first
    command_booking_router,
    command_my_books_router,
    command_paysupport_router,
    command_privacy_router,
    command_settings_router,
)

user_routers = Router()
user_routers.include_routers(
    my_books_routers,
    settings_routers,
    # search_routers,  # Must be the latest
)
