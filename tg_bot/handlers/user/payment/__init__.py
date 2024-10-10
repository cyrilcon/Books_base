__all__ = ("payment_routers",)

from aiogram import Router

from .premium import payment_premium_router

payment_routers = Router()
payment_routers.include_routers(
    payment_premium_router,
)
