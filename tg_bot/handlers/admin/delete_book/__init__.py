__all__ = (
    "command_delete_book_router",
    "delete_book_routers",
)

from aiogram import Router

from .delete_book import command_delete_book_router
from .delete_book_cancel import delete_book_cancel_router
from .delete_book_process import delete_book_process_router

delete_book_routers = Router()
delete_book_routers.include_routers(
    delete_book_cancel_router,
    delete_book_process_router,
)
