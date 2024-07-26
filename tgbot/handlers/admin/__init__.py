from aiogram import Router

from .add_admin import add_admin_routers
from .admin import admin_router

admin_routers = Router()
admin_routers.include_routers(
    admin_router,
    add_admin_routers,
)
