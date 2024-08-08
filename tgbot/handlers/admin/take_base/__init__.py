from aiogram import Router

from .take_base_1_select_user import take_base_router_1
from .take_base_2_take_away_base import take_base_router_2
from .take_base_cancel import take_base_cancel_router

take_base_routers = Router()
take_base_routers.include_routers(
    take_base_cancel_router,
    take_base_router_1,
    take_base_router_2,
)
