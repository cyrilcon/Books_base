from fastapi import APIRouter

from config import config
from .admins import admins_router
from .articles import articles_router
from .authors import authors_router
from .blacklist import blacklist_router
from .books import books_router
from .discounts import discounts_router
from .genres import genres_router
from .orders import orders_router
from .payments import payments_router
from .premium import premium_router
from .users import users_router

routers_list = [
    admins_router,
    articles_router,
    authors_router,
    blacklist_router,
    books_router,
    discounts_router,
    genres_router,
    orders_router,
    payments_router,
    premium_router,
    users_router,
]

routers = APIRouter(
    prefix=config.api.v1.prefix,
)
for router in routers_list:
    routers.include_router(router)
