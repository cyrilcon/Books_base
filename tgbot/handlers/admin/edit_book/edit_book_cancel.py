from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import EditBook

edit_book_cancel_router = Router()
edit_book_cancel_router.message.filter(AdminFilter())
edit_book_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("edit-book-cancel")
)


@edit_book_cancel_router.callback_query(StateFilter(EditBook), F.data == "cancel")
async def edit_book_cancel():
    pass
