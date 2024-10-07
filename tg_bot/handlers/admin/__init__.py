__all__ = ("admin_routers",)

from aiogram import Router

from tg_bot.filters import SuperAdminFilter, AdminFilter
from tg_bot.middlewares import ResetStateMiddleware
from .add_admin import command_add_admin_router, add_admin_routers
from .add_blacklist import command_add_blacklist_router, add_blacklist_routers
from .admin import command_admin_router
from .remove_admin import command_remove_admin_router, remove_admin_routers
from .remove_blacklist import command_remove_blacklist_router, remove_blacklist_routers
from .stats import command_stats_router

supper_admin_commands_router = Router()
supper_admin_commands_router.message.filter(SuperAdminFilter())
supper_admin_commands_router.include_routers(
    command_add_admin_router,
    command_remove_admin_router,
)

admin_commands_router = Router()
admin_commands_router.message.middleware(ResetStateMiddleware())
admin_commands_router.include_routers(
    command_admin_router,  # Must be the first
    supper_admin_commands_router,
    command_add_blacklist_router,
    command_remove_blacklist_router,
    command_stats_router,
)

admin_routers = Router()
admin_routers.message.filter(AdminFilter())
admin_routers.include_routers(
    admin_commands_router,  # Must be the first
    add_admin_routers,
    add_blacklist_routers,
    remove_admin_routers,
    remove_blacklist_routers,
)
