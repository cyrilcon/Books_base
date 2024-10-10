__all__ = (
    "command_cancel_premium_router",
    "cancel_premium_routers",
)

from aiogram import Router

from .cancel_premium import command_cancel_premium_router
from .cancel_premium_cancel import cancel_premium_cancel_router
from .cancel_premium_process import cancel_premium_process_router

cancel_premium_routers = Router()
cancel_premium_routers.include_routers(
    cancel_premium_cancel_router,
    cancel_premium_process_router,
)
