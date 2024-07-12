from aiogram import Router

from .remove_admin import remove_admin_router
from .remove_admin_cancel import remove_admin_cancel_router

remove_admin_routers = Router()
remove_admin_routers.include_routers(
    remove_admin_cancel_router,
    remove_admin_router,
)
