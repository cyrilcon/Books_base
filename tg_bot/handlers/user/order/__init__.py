from aiogram import Router

from .order_again import order_again_router
from .order_cancel import order_cancel_router
from .order_step_1_book_title import order_step_1_router
from .order_step_2_author_name import order_step_2_router

order_routers = Router()
order_routers.include_routers(
    order_again_router,
    order_cancel_router,
    order_step_1_router,
    order_step_2_router,
)
