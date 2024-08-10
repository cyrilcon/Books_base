from aiogram import Router

from .edit_book import edit_book_router
from .edit_book_1_article import edit_book_router_1
from .edit_book_2_title import edit_book_router_2

# from .edit_book_3_authors import edit_book_router_3
# from .edit_book_4_description import edit_book_router_4
# from .edit_book_5_genres import edit_book_router_5
# from .edit_book_6_cover import edit_book_router_6
# from .edit_book_7_files import edit_book_router_7
# from .edit_book_8_price import edit_book_router_8
from .edit_book_cancel import edit_book_cancel_router

edit_book_routers = Router()
edit_book_routers.include_routers(
    edit_book_cancel_router,
    edit_book_router,
    edit_book_router_1,
    edit_book_router_2,
    # edit_book_router_3,
    # edit_book_router_4,
    # edit_book_router_5,
    # edit_book_router_6,
    # edit_book_router_7,
    # edit_book_router_8,
)
