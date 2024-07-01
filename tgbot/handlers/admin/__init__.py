from aiogram import Router

from .add_book import add_book_routers
from .add_to_blacklist import add_to_blacklist_routers
from .admin import admin_router
from .check_booking import check_booking_router
from .delete_book import delete_book_routers
from .edit_book import edit_book_routers
from .send_files import send_files_routers
from .send_message import send_message_routers

admin_routers = Router()
admin_routers.include_routers(
    admin_router,
    add_book_routers,
    add_to_blacklist_routers,
    check_booking_router,
    delete_book_routers,
    edit_book_routers,
    send_files_routers,
    send_message_routers,
)
