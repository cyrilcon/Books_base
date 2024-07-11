from aiogram import Router

from .add_admin import add_admin_routers
from .add_blacklist import add_blacklist_routers
from .add_book import add_book_routers
from .admin import admin_router
from .check_booking import check_booking_router
from .delete_book import delete_book_routers
from .edit_book import edit_book_routers
from .remove_blacklist import remove_blacklist_routers
from .send_files import send_files_routers
from .send_message import send_message_routers

admin_routers = Router()
admin_routers.include_routers(
    admin_router,
    add_admin_routers,
    add_blacklist_routers,
    add_book_routers,
    check_booking_router,
    delete_book_routers,
    edit_book_routers,
    remove_blacklist_routers,
    send_files_routers,
    send_message_routers,
)
