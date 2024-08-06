from aiogram import Router

from .add_admin import add_admin_routers
from .add_blacklist import add_blacklist_routers
from .add_book import add_book_routers
from .admin import admin_router
from .cancel_premium import cancel_premium_routers
from .check_booking import check_booking_router
from .give_premium import give_premium_routers
from .remove_admin import remove_admin_routers
from .remove_blacklist import remove_blacklist_routers
from .send_files import send_files_routers
from .send_message import send_message_routers
from .serve import serve_routers

admin_routers = Router()
admin_routers.include_routers(
    admin_router,  # Must be the first
    add_admin_routers,
    add_blacklist_routers,
    add_book_routers,
    cancel_premium_routers,
    check_booking_router,
    give_premium_routers,
    remove_admin_routers,
    remove_blacklist_routers,
    send_files_routers,
    send_message_routers,
    serve_routers,
)
