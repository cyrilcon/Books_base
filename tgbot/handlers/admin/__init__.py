from aiogram import Router

from tgbot.filters import AdminFilter
from .add_admin import add_admin_routers
from .add_blacklist import add_blacklist_routers
from .add_book import add_book_routers
from .admin import admin_router
from .cancel_premium import cancel_premium_routers
from .delete_book import delete_book_routers
from .edit_book import edit_book_routers
from .give_base import give_base_routers
from .give_premium import give_premium_routers
from .remove_admin import remove_admin_routers
from .remove_blacklist import remove_blacklist_routers
from .send_book import send_book_routers
from .send_message import send_message_routers
from .serve_order import serve_order_routers
from .take_base import take_base_routers
from .view_orders import view_orders_router

admin_routers = Router()
admin_routers.message.filter(AdminFilter())
admin_routers.include_routers(
    admin_router,  # Must be the first
    add_admin_routers,
    add_blacklist_routers,
    add_book_routers,
    cancel_premium_routers,
    delete_book_routers,
    # edit_book_routers,
    give_base_routers,
    give_premium_routers,
    remove_admin_routers,
    remove_blacklist_routers,
    send_book_routers,
    send_message_routers,
    serve_order_routers,
    take_base_routers,
    view_orders_router,
)
