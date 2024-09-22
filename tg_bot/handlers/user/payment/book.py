from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message
from fluent.runtime import FluentLocalization

from tg_bot.enums import MessageEffect
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.schemas import PaymentCurrencyEnum, PaymentTypeEnum
from tg_bot.services import get_user_localization, ClearKeyboard
from tg_bot.api.books_base_api import api
from tg_bot.config import config
from tg_bot.services import Payment, create_user_link
from tg_bot.states import Payment as PaymentState

payment_book_router = Router()


@payment_book_router.callback_query(F.data.startswith("buy"))
async def payment_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    price = int(call.data.split(":")[-2])
    id_book = call.data.split(":")[-1]

    if price == 85:
        # TODO: проверить скидку у пользователя и от этого выдавать цену
        pass
