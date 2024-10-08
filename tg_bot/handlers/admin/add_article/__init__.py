__all__ = (
    "command_add_article_router",
    "add_article_routers",
)

from aiogram import Router

from .add_article import command_add_article_router
from .add_article_cancel import add_article_cancel_router
from .add_article_step_1_title import add_article_step_1_router
from .add_article_step_2_link import add_article_step_2_router
from .add_article_step_3_language_code import add_article_step_3_router

add_article_routers = Router()
add_article_routers.include_routers(
    add_article_cancel_router,
    add_article_step_1_router,
    add_article_step_2_router,
    add_article_step_3_router,
)
