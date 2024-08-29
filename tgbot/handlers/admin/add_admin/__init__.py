from aiogram import Router

from tgbot.filters import SuperAdminFilter
from .add_admin import add_admin_router
from .add_admin_cancel import add_admin_cancel_router

add_admin_routers = Router()
add_admin_routers.message.filter(SuperAdminFilter())
add_admin_routers.include_routers(
    add_admin_cancel_router,
    add_admin_router,
)
