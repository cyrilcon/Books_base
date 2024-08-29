"""Import all routers and add them to routers_list."""

from .user import user_routers
from .admin import admin_routers

routers_list = [
    admin_routers,
    user_routers,
]

__all__ = ("routers_list",)
