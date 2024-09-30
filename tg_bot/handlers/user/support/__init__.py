from aiogram import Router

from tg_bot.middlewares import BlacklistMiddleware
from .support import support_router
from .support_cancel import support_cancel_router
from .support_reply_to_admin import support_reply_to_admin_router
from .support_reply_to_user import support_reply_to_user_router

support_routers = Router()
support_routers.message.middleware(BlacklistMiddleware())
support_routers.callback_query.middleware(BlacklistMiddleware())
support_routers.include_routers(
    support_cancel_router,
    support_router,
    support_reply_to_admin_router,
    support_reply_to_user_router,
)
