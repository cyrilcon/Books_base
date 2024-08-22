from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import RemoveBlacklist

remove_blacklist_cancel_router = Router()
remove_blacklist_cancel_router.message.filter(AdminFilter())
remove_blacklist_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("remove-blacklist-canceled")
)


@remove_blacklist_cancel_router.callback_query(
    StateFilter(RemoveBlacklist), F.data == "cancel"
)
async def remove_blacklist_cancel():
    pass
