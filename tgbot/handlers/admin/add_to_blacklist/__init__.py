from aiogram import Router

from .add_to_blacklist import add_to_blacklist_router
from .add_to_blacklist_cancel import add_to_blacklist_cancel_router

add_to_blacklist_routers = Router()
add_to_blacklist_routers.include_routers(
    add_to_blacklist_cancel_router,
    add_to_blacklist_router,
)
