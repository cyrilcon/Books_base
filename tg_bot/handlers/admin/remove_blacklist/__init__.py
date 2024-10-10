__all__ = (
    "command_remove_blacklist_router",
    "remove_blacklist_routers",
)

from aiogram import Router

from .remove_blacklist import command_remove_blacklist_router
from .remove_blacklist_cancel import remove_blacklist_cancel_router
from .remove_blacklist_process import remove_blacklist_process_router

remove_blacklist_routers = Router()
remove_blacklist_routers.include_routers(
    remove_blacklist_cancel_router,
    remove_blacklist_process_router,
)
