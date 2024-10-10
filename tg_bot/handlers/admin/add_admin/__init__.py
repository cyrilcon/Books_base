__all__ = (
    "command_add_admin_router",
    "add_admin_routers",
)

from aiogram import Router

from .add_admin import command_add_admin_router
from .add_admin_cancel import add_admin_cancel_router
from .add_admin_process import add_admin_process_router

add_admin_routers = Router()
add_admin_routers.include_routers(
    add_admin_cancel_router,
    add_admin_process_router,
)
