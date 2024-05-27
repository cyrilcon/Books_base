from aiogram import Router

from .support import support_router
from .support_cancel import support_cancel_router
from .support_reply_to_user import support_reply_to_user_router

support_routers = Router()
support_routers.include_routers(
    support_cancel_router,
    support_reply_to_user_router,
    support_router,
)
