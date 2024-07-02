from aiogram import Router

from .remove_from_blacklist import remove_from_blacklist_router
from .remove_from_blacklist_cancel import remove_from_blacklist_cancel_router

remove_from_blacklist_routers = Router()
remove_from_blacklist_routers.include_routers(
    remove_from_blacklist_router,
    remove_from_blacklist_cancel_router,
)
