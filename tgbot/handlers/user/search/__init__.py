from aiogram import Router

from .search_info import search_info_router
from .search_title import search_title_router

search_routers = Router()
search_routers.include_routers(
    search_info_router,
    search_title_router,
)
