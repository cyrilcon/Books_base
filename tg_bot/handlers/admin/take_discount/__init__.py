__all__ = (
    "command_take_discount_router",
    "take_discount_routers",
)

from aiogram import Router

from .take_discount import command_take_discount_router
from .take_discount_cancel import take_discount_cancel_router
from .take_discount_process import take_discount_process_router

take_discount_routers = Router()
take_discount_routers.include_routers(
    take_discount_cancel_router,
    take_discount_process_router,
)
