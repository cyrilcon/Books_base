__all__ = (
    "command_settings_router",
    "settings_routers",
)

from aiogram import Router

from .settings import command_settings_router
from .settings_process import settings_process_router

settings_routers = Router()
settings_routers.include_routers(
    settings_process_router,
)
