from aiogram import Router
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import AddAdmin

add_admin_cancel_router = Router()
add_admin_cancel_router.message.filter(AdminFilter())
add_admin_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("add-admin-cancel")
)


@add_admin_cancel_router.callback_query(StateFilter(AddAdmin))
async def add_admin_cancel():
    """
    Cancels adding a user to the administrator list.
    """

    pass
