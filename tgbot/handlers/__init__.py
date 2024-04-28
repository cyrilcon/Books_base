"""Импортируются все роутеры и добавляются в список routers_list."""

from .admin import admin_routers
from .user import user_routers

routers_list = [
    user_routers,
    admin_routers,
]

# __all__ = [
#     "routers_list",
# ]
