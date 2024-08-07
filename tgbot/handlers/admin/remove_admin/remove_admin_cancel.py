from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import SuperAdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import RemoveAdmin

remove_admin_cancel_router = Router()
remove_admin_cancel_router.message.filter(SuperAdminFilter())
remove_admin_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("remove-admin-cancel")
)


@remove_admin_cancel_router.callback_query(StateFilter(RemoveAdmin), F.data == "cancel")
async def remove_admin_cancel():
    pass
