from aiogram import Router

from tg_bot.middlewares import BlacklistMiddleware
from .share_base_cancel import share_base_cancel_router
from .share_base_step_1_select_user import share_base_step_1_router
from .share_base_step_2_transfer import share_base_step_2_router

share_base_routers = Router()
share_base_routers.message.middleware(BlacklistMiddleware())
share_base_routers.callback_query.middleware(BlacklistMiddleware())
share_base_routers.include_routers(
    share_base_cancel_router,
    share_base_step_1_router,
    share_base_step_2_router,
)
