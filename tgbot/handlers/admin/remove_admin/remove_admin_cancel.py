from aiogram import Router
from aiogram.filters import StateFilter

from tgbot.filters import SuperAdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import RemoveAdmin

remove_admin_cancel_router = Router()
remove_admin_cancel_router.message.filter(SuperAdminFilter())
remove_admin_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("remove-admin-cancel")
)


@remove_admin_cancel_router.callback_query(StateFilter(RemoveAdmin))
async def remove_admin_cancel():
    """
    Repeal of administrator demotion.
    """

    pass
