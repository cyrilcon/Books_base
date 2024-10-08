__all__ = (
    "command_broadcast_router",
    "broadcast_routers",
)

from aiogram import Router

from .broadcast import command_broadcast_router
from .broadcast_cancel import broadcast_cancel_router
from .broadcast_process import broadcast_process_router

broadcast_routers = Router()
broadcast_routers.include_routers(
    broadcast_cancel_router,
    broadcast_process_router,
)
