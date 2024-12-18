__all__ = ("start_routers",)

from aiogram import Router

from .start import command_start_router
from .start_book import start_book_router
from .start_invite import start_invite_router

start_routers = Router()
start_routers.include_routers(
    start_book_router,
    start_invite_router,
    command_start_router,
)
