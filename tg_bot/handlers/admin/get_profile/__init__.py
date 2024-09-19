from aiogram import Router

from .get_profile import get_profile_router
from .get_profile_cancel import get_profile_cancel_router

get_profile_routers = Router()
get_profile_routers.include_routers(
    get_profile_cancel_router,
    get_profile_router,
)
