from aiogram import Router

from tg_bot.middlewares import BlacklistMiddleware
from .cancel_order import cancel_order_router
from .cancel_order_cancel import cancel_order_cancel_router

cancel_order_routers = Router()
cancel_order_routers.message.middleware(BlacklistMiddleware())
cancel_order_routers.callback_query.middleware(BlacklistMiddleware())
cancel_order_routers.include_routers(
    cancel_order_cancel_router,
    cancel_order_router,
)
