"""Импортируются все роутеры и добавляются в список routers_list."""

from .admin import admin_routers
from .echo import echo_router
from .user import user_routers

routers_list = [
    user_routers,
    admin_routers,
    echo_router,  # echo_router должен быть последним
]

# __all__ = [
#     "routers_list",
# ]
