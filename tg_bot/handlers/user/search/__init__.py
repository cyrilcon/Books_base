__all__ = (
    "command_search_router",
    "search_routers",
)

from aiogram import Router

from .search import command_search_router
from .search_by_author import search_by_author_router
from .search_by_genre import search_by_genre_router
from .search_by_title import search_by_title_router
from .search_pagination_info import search_pagination_info_router

search_routers = Router()
search_routers.include_routers(
    search_by_author_router,
    search_by_genre_router,
    search_by_title_router,
    search_pagination_info_router,
)
