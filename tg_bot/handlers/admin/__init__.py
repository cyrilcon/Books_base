__all__ = ("admin_routers",)

from aiogram import Router

from tg_bot.filters import SuperAdminFilter, AdminFilter
from tg_bot.middlewares import ResetStateMiddleware
from .add_admin import command_add_admin_router, add_admin_routers
from .add_article import add_article_routers
from .add_blacklist import add_blacklist_routers
from .add_book import add_book_routers
from .admin import command_admin_router
from .broadcast import broadcast_routers
from .cancel_premium import cancel_premium_routers
from .delete_article import delete_article_routers
from .delete_book import delete_book_routers
from .edit_book import edit_book_routers
from .get_profile import get_profile_routers
from .give_base import give_base_routers
from .give_book import give_book_routers
from .give_discount import give_discount_routers
from .give_premium import give_premium_routers
from .refund import refund_routers
from .remove_admin import command_remove_admin_router, remove_admin_routers
from .remove_blacklist import remove_blacklist_routers
from .send_book import send_book_routers
from .send_message import send_message_routers
from .serve_order import serve_order_routers
from .stats import command_stats_router
from .take_base import take_base_routers
from .take_discount import take_discount_routers
from .view_orders import view_orders_router

supper_admin_commands_router = Router()
supper_admin_commands_router.message.filter(SuperAdminFilter())
supper_admin_commands_router.include_routers(
    command_add_admin_router,
    command_remove_admin_router,
)

admin_commands_router = Router()
admin_commands_router.message.middleware(ResetStateMiddleware())
admin_commands_router.include_routers(
    command_admin_router,  # Must be the first
    supper_admin_commands_router,
    command_stats_router,
)

admin_routers = Router()
admin_routers.message.filter(AdminFilter())
admin_routers.include_routers(
    admin_commands_router,  # Must be the first
    add_admin_routers,
    add_article_routers,
    add_blacklist_routers,
    add_book_routers,
    broadcast_routers,
    cancel_premium_routers,
    delete_article_routers,
    delete_book_routers,
    edit_book_routers,
    get_profile_routers,
    give_base_routers,
    give_book_routers,
    give_discount_routers,
    give_premium_routers,
    refund_routers,
    remove_admin_routers,
    remove_blacklist_routers,
    send_book_routers,
    send_message_routers,
    serve_order_routers,
    take_base_routers,
    take_discount_routers,
    view_orders_router,
)
