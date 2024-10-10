__all__ = (
    "user_commands_router",
    "user_routers",
)

from aiogram import Router

from tg_bot.middlewares import ResetStateMiddleware
from .base_store import command_base_store_router, base_store_routers
from .booking import command_booking_router
from .cancel_order import command_cancel_order_router, cancel_order_routers
from .my_books import command_my_books_router, my_books_routers
from .news import command_news_router, news_routers
from .order import command_order_router, order_routers
from .payment import payment_routers
from .paysupport import command_paysupport_router
from .premium import premium_router
from .privacy import command_privacy_router
from .saturday import command_saturday_router, saturday_routers
from .search import command_search_router, search_routers
from .search import search_routers
from .settings import command_settings_router, settings_routers
from .share_base import common_share_base_router, share_base_routers
from .start import start_routers
from .support import command_support_router, support_routers

user_commands_router = Router()
user_commands_router.message.middleware(ResetStateMiddleware())
user_commands_router.include_routers(
    start_routers,  # Must be the first
    command_base_store_router,
    command_booking_router,
    command_cancel_order_router,
    command_my_books_router,
    command_news_router,
    command_order_router,
    command_paysupport_router,
    command_privacy_router,
    command_saturday_router,
    command_settings_router,
    common_share_base_router,
    command_support_router,
    command_search_router,  # Must be the latest
)

user_routers = Router()
user_routers.include_routers(
    base_store_routers,
    cancel_order_routers,
    my_books_routers,
    news_routers,
    order_routers,
    premium_router,
    saturday_routers,
    payment_routers,
    settings_routers,
    share_base_routers,
    support_routers,
    search_routers,  # Must be the latest
)
