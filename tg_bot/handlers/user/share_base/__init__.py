__all__ = (
    "common_share_base_router",
    "share_base_routers",
)

from aiogram import Router

from .share_base import common_share_base_router
from .share_base_cancel import share_base_cancel_router
from .share_base_step_1_select_user import share_base_step_1_router
from .share_base_step_2_transfer import share_base_step_2_router

share_base_routers = Router()
share_base_routers.include_routers(
    share_base_cancel_router,
    share_base_step_1_router,
    share_base_step_2_router,
)
