from aiogram import Router

from .premium import premium_router
from .premium_paid import premium_paid_router

premium_routers = Router()
premium_routers.include_routers(
    premium_router,
    premium_paid_router,
)
