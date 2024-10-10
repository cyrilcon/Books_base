__all__ = ("routers",)

from aiogram import Router

from .admin import admin_commands_router, admin_routers
from .user import user_commands_router, user_routers

routers = Router()
routers.include_routers(
    admin_commands_router,
    user_commands_router,
    admin_routers,
    user_routers,
)
