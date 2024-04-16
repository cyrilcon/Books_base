from aiogram import Router

from .add_book import add_book_router
from .admin import admin_router

admin_routers = Router()
admin_routers.include_routers(
    admin_router,
    add_book_router,
)
