from aiogram import Router

from .book import payment_book_router
from .premium import payment_premium_router
from .read import read_router

payment_routers = Router()
payment_routers.include_routers(
    payment_book_router,
    payment_premium_router,
    read_router,
)
