__all__ = (
    "command_give_premium_router",
    "give_premium_routers",
)

from aiogram import Router

from .give_premium import command_give_premium_router
from .give_premium_cancel import give_premium_cancel_router
from .give_premium_process import give_premium_process_router

give_premium_routers = Router()
give_premium_routers.include_routers(
    give_premium_cancel_router,
    give_premium_process_router,
)
