__all__ = (
    "command_edit_book_router",
    "edit_book_routers",
)

from aiogram import Router

from .edit_book import command_edit_book_router
from .edit_book_1_article import edit_article_router
from .edit_book_2_title import edit_title_router
from .edit_book_3_authors import edit_authors_router
from .edit_book_4_description import edit_description_router
from .edit_book_5_genres import edit_genres_router
from .edit_book_6_cover import edit_cover_router
from .edit_book_7_files import edit_files_router
from .edit_book_8_price import edit_price_router
from .edit_book_cancel import edit_book_cancel_router
from .edit_book_process import edit_book_process_router

edit_book_routers = Router()
edit_book_routers.include_routers(
    edit_book_cancel_router,
    edit_book_process_router,
    edit_article_router,
    edit_title_router,
    edit_authors_router,
    edit_description_router,
    edit_genres_router,
    edit_cover_router,
    edit_files_router,
    edit_price_router,
)
