from aiogram import Router

from .add_book_1 import add_book_router_1
from .add_book_cancel import add_book_cancel_router

add_book_routers = Router()
add_book_routers.include_routers(
    add_book_cancel_router,
    add_book_router_1,
)
