from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import SuperAdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import Serve

serve_cancel_router = Router()
serve_cancel_router.message.filter(SuperAdminFilter())
serve_cancel_router.callback_query.middleware(CancelCommandMiddleware("serve-cancel"))


@serve_cancel_router.callback_query(StateFilter(Serve), F.data == "cancel")
async def serve_cancel():
    """
    Cancellation of booking service.
    """

    pass
