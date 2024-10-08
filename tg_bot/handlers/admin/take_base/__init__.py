__all__ = (
    "command_take_base_router",
    "take_base_routers",
)

from aiogram import Router

from .take_base import command_take_base_router
from .take_base_cancel import take_base_cancel_router
from .take_base_step_1_select_user import take_base_step_1_router
from .take_base_step_2_deduct_base import take_base_step_2_router

take_base_routers = Router()
take_base_routers.include_routers(
    take_base_cancel_router,
    take_base_step_1_router,
    take_base_step_2_router,
)
