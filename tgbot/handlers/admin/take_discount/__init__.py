from aiogram import Router

from .take_discount import take_discount_router
from .take_discount_cancel import take_discount_cancel_router

take_discount_routers = Router()
take_discount_routers.include_routers(
    take_discount_cancel_router,
    take_discount_router,
)
