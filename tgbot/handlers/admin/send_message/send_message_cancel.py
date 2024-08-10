from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import SendMessage

send_message_cancel_router = Router()
send_message_cancel_router.message.filter(AdminFilter())
send_message_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("send-message-cancel")
)


@send_message_cancel_router.callback_query(StateFilter(SendMessage), F.data == "cancel")
async def send_message_cancel():
    pass
