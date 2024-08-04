from aiogram import Router

from .add_book_1_article import add_book_router_1
from .add_book_2_title import add_book_router_2
from .add_book_3_authors import add_book_router_3
from .add_book_4_description import add_book_router_4
from .add_book_5_genres import add_book_router_5
from .add_book_6_cover import add_book_router_6
from .add_book_7_files import add_book_router_7
from .add_book_8_price import add_book_router_8
from .add_book_9_demo_post import add_book_router_9
from .add_book_cancel import add_book_cancel_router

add_book_routers = Router()
add_book_routers.include_routers(
    add_book_cancel_router,
    add_book_router_1,
    add_book_router_2,
    add_book_router_3,
    add_book_router_4,
    add_book_router_5,
    add_book_router_6,
    add_book_router_7,
    add_book_router_8,
    add_book_router_9,
)
