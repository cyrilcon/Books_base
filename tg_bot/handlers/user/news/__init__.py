__all__ = (
    "command_news_router",
    "news_routers",
)

from aiogram import Router

from .news import command_news_router
from .news_position import news_position_router

news_routers = Router()
news_routers.include_routers(
    news_position_router,
)
