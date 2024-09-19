from aiogram import Router

from .broadcast import broadcast_router
from .broadcast_cancel import broadcast_cancel_router

broadcast_routers = Router()
broadcast_routers.include_routers(
    broadcast_cancel_router,
    broadcast_router,
)
