from aiogram import Router

from .send_files_1_select_user import send_files_router_1
from .send_files_2_upload_files import send_files_router_2
from .send_files_3_write_caption import send_files_router_3
from .send_files_cancel import send_files_cancel_router

send_files_routers = Router()
send_files_routers.include_routers(
    send_files_cancel_router,
    send_files_router_1,
    send_files_router_2,
    send_files_router_3,
)
