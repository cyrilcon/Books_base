__all__ = (
    "command_get_token_router",
    "get_token_routers",
)

from aiogram import Router

from .get_token import command_get_token_router
from .get_token_cancel import get_token_cancel_router
from .get_token_process import get_token_process_router

get_token_routers = Router()
get_token_routers.include_routers(
    get_token_cancel_router,
    get_token_process_router,
)
