from aiogram import Router

from .add_admin import add_admin_router
from .add_admin_cancel import add_admin_cancel_router

add_admin_routers = Router()
add_admin_routers.include_routers(
    add_admin_cancel_router,
    add_admin_router,
)
