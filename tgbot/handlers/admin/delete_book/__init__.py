from aiogram import Router

from .delete_book import delete_book_router
from .delete_cancel import delete_book_cancel_router

delete_book_routers = Router()
delete_book_routers.include_routers(
    delete_book_cancel_router,
    delete_book_router,
)
