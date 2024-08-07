from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import AddBlacklist

add_blacklist_cancel_router = Router()
add_blacklist_cancel_router.message.filter(AdminFilter())
add_blacklist_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("add-blacklist-cancel")
)


@add_blacklist_cancel_router.callback_query(
    StateFilter(AddBlacklist), F.data == "cancel"
)
async def add_blacklist_cancel():
    pass
