from aiogram import Router

from .send_book_1_select_user import send_book_router_1
from .send_book_2_select_book import send_book_router_2
from .send_book_cancel import send_book_cancel_router

send_book_routers = Router()
send_book_routers.include_routers(
    send_book_cancel_router,
    send_book_router_1,
    send_book_router_2,
)
