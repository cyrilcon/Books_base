from aiogram import Router

from .share_base_1_select_user import share_base_router_1
from .share_base_2_send_base import share_base_router_2
from .share_base_cancel import share_base_cancel_router

share_base_routers = Router()
share_base_routers.include_routers(
    share_base_cancel_router,
    share_base_router_1,
    share_base_router_2,
)
