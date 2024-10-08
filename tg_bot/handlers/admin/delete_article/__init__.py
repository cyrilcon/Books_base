__all__ = (
    "command_delete_article_router",
    "delete_article_routers",
)

from aiogram import Router

from .delete_article import command_delete_article_router
from .delete_article_cancel import delete_article_cancel_router
from .delete_article_process import delete_article_process_router

delete_article_routers = Router()
delete_article_routers.include_routers(
    delete_article_cancel_router,
    delete_article_process_router,
)
