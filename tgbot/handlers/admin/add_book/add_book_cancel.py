from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import AddBook

add_book_cancel_router = Router()
add_book_cancel_router.message.filter(AdminFilter())
add_book_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("add-book-cancel")
)


@add_book_cancel_router.callback_query(StateFilter(AddBook), F.data == "cancel")
async def add_book_cancel():
    pass
