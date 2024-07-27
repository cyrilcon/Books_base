from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import GivePremium

give_premium_cancel_router = Router()
give_premium_cancel_router.message.filter(AdminFilter())
give_premium_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("give-premium-cancel")
)


@give_premium_cancel_router.callback_query(StateFilter(GivePremium), F.data == "cancel")
async def give_premium_cancel():
    """
    Revocation of Books_base Premium status.
    """

    pass
