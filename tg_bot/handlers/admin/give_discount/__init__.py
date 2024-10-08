__all__ = (
    "command_give_discount_router",
    "give_discount_routers",
)

from aiogram import Router

from .give_discount import command_give_discount_router
from .give_discount_cancel import give_discount_cancel_router
from .give_discount_step_1_select_user import give_discount_step_1_router
from .give_discount_step_2_select_discount import give_discount_step_2_router

give_discount_routers = Router()
give_discount_routers.include_routers(
    give_discount_cancel_router,
    give_discount_step_1_router,
    give_discount_step_2_router,
)
