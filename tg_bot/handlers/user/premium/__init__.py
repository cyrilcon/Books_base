from aiogram import Router

from .premium import premium_router
from .premium_cancel_payment import premium_cancel_payment_router
from .premium_check_payment import premium_paid_router

premium_routers = Router()
premium_routers.include_routers(
    premium_router,
    premium_cancel_payment_router,
    premium_paid_router,
)
