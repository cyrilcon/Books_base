from aiogram import Router

from .add_book_cancel import add_book_cancel_router
from .add_book_step_1_article import add_book_step_1_router
from .add_book_step_2_title import add_book_step_2_router
from .add_book_step_3_authors import add_book_step_3_router
from .add_book_step_4_description import add_book_step_4_router
from .add_book_step_5_genres import add_book_step_5_router
from .add_book_step_6_cover import add_book_step_6_router
from .add_book_step_7_files import add_book_step_7_router
from .add_book_step_8_price import add_book_step_8_router
from .add_book_step_9_demo_post import add_book_step_9_router

add_book_routers = Router()
add_book_routers.include_routers(
    add_book_cancel_router,
    add_book_step_1_router,
    add_book_step_2_router,
    add_book_step_3_router,
    add_book_step_4_router,
    add_book_step_5_router,
    add_book_step_6_router,
    add_book_step_7_router,
    add_book_step_8_router,
    add_book_step_9_router,
)
