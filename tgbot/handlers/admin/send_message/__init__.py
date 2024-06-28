from aiogram import Router

from .send_message_1_select_user import send_message_router_1
from .send_message_2_write_message import send_message_router_2
from .send_message_cancel import send_message_cancel_router

send_message_routers = Router()
send_message_routers.include_routers(
    send_message_cancel_router,
    send_message_router_1,
    send_message_router_2,
)
