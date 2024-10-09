__all__ = (
    "command_view_orders_router",
    "view_orders_routers",
)

from aiogram import Router

from .view_order_position import view_order_position_router
from .view_orders import command_view_orders_router

view_orders_routers = Router()
view_orders_routers.include_routers(
    view_order_position_router,
)
