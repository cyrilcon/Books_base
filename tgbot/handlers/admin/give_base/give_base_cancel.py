from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import GiveBase

give_base_cancel_router = Router()
give_base_cancel_router.message.filter(AdminFilter())
give_base_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("give-base-cancel")
)


@give_base_cancel_router.callback_query(StateFilter(GiveBase), F.data == "cancel")
async def give_base_cancel():
    pass
