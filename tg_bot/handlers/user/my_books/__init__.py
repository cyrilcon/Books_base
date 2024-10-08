__all__ = (
    "command_my_books_router",
    "my_books_routers",
)

from aiogram import Router

from .my_books import command_my_books_router
from .my_books_page import my_books_page_router

my_books_routers = Router()
my_books_routers.include_routers(
    my_books_page_router,
)
