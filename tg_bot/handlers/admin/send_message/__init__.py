__all__ = (
    "command_send_message_router",
    "send_message_routers",
)

from aiogram import Router

from .send_message import command_send_message_router
from .send_message_cancel import send_message_cancel_router
from .send_message_step_1_select_user import send_message_step_1_router
from .send_message_step_2_write_message import send_message_step_2_router

send_message_routers = Router()
send_message_routers.include_routers(
    send_message_cancel_router,
    send_message_step_1_router,
    send_message_step_2_router,
)
