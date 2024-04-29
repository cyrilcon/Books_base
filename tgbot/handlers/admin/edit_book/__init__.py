from aiogram import Router

from .edit_book import edit_book_router
from .edit_book_cancel import update_book_cancel_router

edit_book_routers = Router()
edit_book_routers.include_routers(
    update_book_cancel_router,
    edit_book_router,
)
