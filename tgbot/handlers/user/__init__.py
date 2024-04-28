from aiogram import Router

from .search import search_title_router
from .start import start_router

user_routers = Router()
user_routers.include_routers(
    start_router,
    search_title_router,
)
