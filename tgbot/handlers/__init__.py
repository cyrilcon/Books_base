"""Import all routers and add them to routers_list."""

from .user import user_routers

routers_list = [
    user_routers,
]

__all__ = [
    "routers_list",
]
