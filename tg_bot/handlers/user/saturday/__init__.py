__all__ = (
    "command_saturday_router",
    "saturday_routers",
)

from aiogram import Router

from tg_bot.middlewares import SaturdayMiddleware
from .saturday import command_saturday_router
from .saturday_cancel import saturday_cancel_router
from .saturday_step_1 import saturday_step_1_router
from .saturday_step_2 import saturday_step_2_router
from .saturday_step_3 import saturday_step_3_router

saturday_routers = Router()
saturday_routers.message.middleware(SaturdayMiddleware())
saturday_routers.callback_query.middleware(SaturdayMiddleware())
saturday_routers.include_routers(
    saturday_cancel_router,
    saturday_step_1_router,
    saturday_step_2_router,
    saturday_step_3_router,
)
