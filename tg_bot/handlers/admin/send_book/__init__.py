__all__ = (
    "comment_send_book_router",
    "send_book_routers",
)

from aiogram import Router

from .send_book import comment_send_book_router
from .send_book_cancel import send_book_cancel_router
from .send_book_step_1_select_user import send_book_step_1_router
from .send_book_step_2_select_book import send_book_step_2_router

send_book_routers = Router()
send_book_routers.include_routers(
    send_book_cancel_router,
    send_book_step_1_router,
    send_book_step_2_router,
)
