from aiogram import Router

from .give_base_cancel import give_base_cancel_router
from .give_base_step_1_select_user import give_base_step_1_router
from .give_base_step_2_transfer import give_base_step_2_router

give_base_routers = Router()
give_base_routers.include_routers(
    give_base_cancel_router,
    give_base_step_1_router,
    give_base_step_2_router,
)
