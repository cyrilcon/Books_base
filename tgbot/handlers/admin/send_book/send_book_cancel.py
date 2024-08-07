from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import SendBook

send_book_cancel_router = Router()
send_book_cancel_router.message.filter(AdminFilter())
send_book_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("send-book-cancel")
)


@send_book_cancel_router.callback_query(StateFilter(SendBook), F.data == "cancel")
async def send_book_cancel():
    pass
