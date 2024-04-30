from aiogram import Router

from .search import search_routers
from .start import start_router

user_routers = Router()
user_routers.include_routers(
    start_router,
    search_routers,
)
