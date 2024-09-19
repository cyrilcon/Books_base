from aiogram import Router

from .give_premium import give_premium_router
from .give_premium_cancel import give_premium_cancel_router

give_premium_routers = Router()
give_premium_routers.include_routers(
    give_premium_cancel_router,
    give_premium_router,
)
