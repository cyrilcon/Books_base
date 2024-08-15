from aiogram import Router

from .search import search_router
from .search_by_title import search_by_title_router
from .search_info import search_info_router

search_routers = Router()
search_routers.include_routers(
    search_router,
    search_by_title_router,
    search_info_router,
)
