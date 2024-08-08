from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import SuperAdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import DeleteBook

delete_book_cancel_router = Router()
delete_book_cancel_router.message.filter(SuperAdminFilter())
delete_book_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("delete-book-cancel")
)


@delete_book_cancel_router.callback_query(StateFilter(DeleteBook), F.data == "cancel")
async def delete_book_cancel():
    pass
