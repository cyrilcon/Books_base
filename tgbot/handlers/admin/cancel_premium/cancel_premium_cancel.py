from aiogram import Router
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import CancelPremium

cancel_premium_cancel_router = Router()
cancel_premium_cancel_router.message.filter(AdminFilter())
cancel_premium_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("cancel-premium-cancel")
)


@cancel_premium_cancel_router.callback_query(StateFilter(CancelPremium))
async def cancel_premium_cancel():
    """
    Cancellation of Books_base Premium status.
    """

    pass
