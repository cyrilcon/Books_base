from aiogram import Router

from .remove_blacklist import remove_blacklist_router
from .remove_blacklist_cancel import remove_blacklist_cancel_router

remove_blacklist_routers = Router()
remove_blacklist_routers.include_routers(
    remove_blacklist_cancel_router,
    remove_blacklist_router,
)
