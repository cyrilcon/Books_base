__all__ = (
    "command_give_book_router",
    "give_book_routers",
)

from aiogram import Router

from .give_book import command_give_book_router
from .give_book_cacnel import give_book_cancel_router
from .give_book_step_1_select_user import give_book_step_1_router
from .give_book_step_2_select_book import give_book_step_2_router

give_book_routers = Router()
give_book_routers.include_routers(
    give_book_cancel_router,
    give_book_step_1_router,
    give_book_step_2_router,
)
