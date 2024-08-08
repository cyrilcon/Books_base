from aiogram import Router, F
from aiogram.filters import StateFilter

from tgbot.filters import AdminFilter
from tgbot.middlewares import CancelCommandMiddleware
from tgbot.states import TakeBase

take_base_cancel_router = Router()
take_base_cancel_router.message.filter(AdminFilter())
take_base_cancel_router.callback_query.middleware(
    CancelCommandMiddleware("take-base-cancel")
)


@take_base_cancel_router.callback_query(StateFilter(TakeBase), F.data == "cancel")
async def take_base_cancel():
    pass
