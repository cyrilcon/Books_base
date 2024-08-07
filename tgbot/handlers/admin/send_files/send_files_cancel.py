from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import SuperAdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import SendFiles

send_files_cancel_router = Router()
send_files_cancel_router.message.filter(SuperAdminFilter())
send_files_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("send-files-cancel")
)


@send_files_cancel_router.callback_query(StateFilter(SendFiles), F.data == "cancel")
async def send_files_cancel():
    pass
