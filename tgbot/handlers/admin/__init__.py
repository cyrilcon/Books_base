from aiogram import Router

from .add_admin import add_admin_routers
from .admin import admin_router
from .cancel_premium import cancel_premium_routers
from .give_premium import give_premium_routers
from .remove_admin import remove_admin_routers

admin_routers = Router()
admin_routers.include_routers(
    admin_router,
    add_admin_routers,
    cancel_premium_routers,
    give_premium_routers,
    remove_admin_routers,
)
