from aiogram import Router

from .admin import admin_router

admin_routers = Router()
admin_routers.include_routers(
    admin_router,
)
