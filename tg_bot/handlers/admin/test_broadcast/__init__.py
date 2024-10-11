__all__ = (
    "command_test_broadcast_router",
    "test_broadcast_routers",
)

from aiogram import Router

from .test_broadcast import command_test_broadcast_router
from .test_broadcast_cancel import test_broadcast_cancel_router
from .test_broadcast_process import test_broadcast_process_router

test_broadcast_routers = Router()
test_broadcast_routers.include_routers(
    test_broadcast_cancel_router,
    test_broadcast_process_router,
)
