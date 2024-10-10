__all__ = (
    "command_get_profile_router",
    "get_profile_routers",
)

from aiogram import Router

from .get_profile import command_get_profile_router
from .get_profile_cancel import get_profile_cancel_router
from .get_profile_process import get_profile_process_router

get_profile_routers = Router()
get_profile_routers.include_routers(
    get_profile_cancel_router,
    get_profile_process_router,
)
