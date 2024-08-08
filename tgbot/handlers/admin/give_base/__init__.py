from aiogram import Router

from .give_base_1_select_user import give_base_router_1
from .give_base_2_send_base import give_base_router_2
from .give_base_cancel import give_base_cancel_router

give_base_routers = Router()
give_base_routers.include_routers(
    give_base_cancel_router,
    give_base_router_1,
    give_base_router_2,
)
