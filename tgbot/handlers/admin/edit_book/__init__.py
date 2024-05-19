from aiogram import Router

from .edit_book import edit_book_router
from .edit_book_1_article import edit_book_1_article_router
from .edit_book_2_title import edit_book_2_title_router
from .edit_book_cancel import edit_book_cancel_router

edit_book_routers = Router()
edit_book_routers.include_routers(
    edit_book_cancel_router,
    edit_book_router,
    edit_book_1_article_router,
    edit_book_2_title_router,
)
