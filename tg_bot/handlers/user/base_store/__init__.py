from aiogram import Router

from tg_bot.middlewares import BlacklistMiddleware
from .base_store import base_store_router
from .base_store_cancel_discount import base_store_cancel_discount_router

base_store_routers = Router()
base_store_routers.message.middleware(BlacklistMiddleware())
base_store_routers.callback_query.middleware(BlacklistMiddleware())
base_store_routers.include_routers(
    base_store_router,
    base_store_cancel_discount_router,
)
