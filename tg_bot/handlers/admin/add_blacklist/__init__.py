from aiogram import Router

from .add_blacklist import add_blacklist_router
from .add_blacklist_cancel import add_blacklist_cancel_router

add_blacklist_routers = Router()
add_blacklist_routers.include_routers(
    add_blacklist_cancel_router,
    add_blacklist_router,
)
