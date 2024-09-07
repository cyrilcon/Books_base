from aiogram import Router

from .base_store import base_store_router
from .base_store_exchange import base_store_exchange_router

base_store_routers = Router()
base_store_routers.include_routers(
    base_store_router,
    base_store_exchange_router,
)
