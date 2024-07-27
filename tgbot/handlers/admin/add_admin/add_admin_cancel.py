from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import SuperAdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import AddAdmin

add_admin_cancel_router = Router()
add_admin_cancel_router.message.filter(SuperAdminFilter())
add_admin_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("add-admin-cancel")
)


@add_admin_cancel_router.callback_query(StateFilter(AddAdmin), F.data == "cancel")
async def add_admin_cancel():
    """
    Cancels adding a user to the administrator list.
    """

    pass
