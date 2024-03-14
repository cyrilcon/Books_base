"""Импортируются все роутеры и добавляются в список routers_list."""

from .admin import admin_router
from .echo import echo_router
from .user import start_router

routers_list = [
    admin_router,
    start_router,
    echo_router,  # echo_router должен быть последним
]

# __all__ = [
#     "routers_list",
# ]
