__all__ = ("start_routers",)

from aiogram import Router

from .start import command_start_router
from .start_deep_link import start_deep_link_router

start_routers = Router()
start_routers.include_routers(
    start_deep_link_router,
    command_start_router,
)
