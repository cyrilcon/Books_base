from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, LabeledPrice
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from config import config
from services import ClearKeyboard
from tg_bot.api.books_base_api import api
from tg_bot.keyboards.inline.keyboards import pay_premium_keyboard
from tg_bot.services import Payment
from tg_bot.states import Payment as PaymentState

premium_router = Router()
premium_router.message.middleware(ChatActionMiddleware())


@premium_router.message(Command("premium"), flags={"chat_action": "typing"})
async def premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    id_user = message.from_user.id
    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.is_premium:
        await message.answer(
            l10n.format_value("premium-error-user-already-has-premium")
        )
        return

    price_rub = config.price.premium.rub
    price_stars = config.price.premium.stars

    payment = Payment(
        amount=price_rub,
        comment="Books_base Premium",
    )
    payment.create()

    sent_message = await message.answer_invoice(
        title="Books_base Premium ⚜️",
        description=l10n.format_value(
            "premium", {"price_rub": price_rub, "price_stars": price_stars}
        ),
        prices=[LabeledPrice(label="XTR", amount=price_stars)],
        provider_token="",
        payload="premium",
        currency="XTR",
        reply_markup=pay_premium_keyboard(
            l10n=l10n,
            url_payment=payment.invoice,
            currency="XTR",
            price_stars=price_stars,
            price_rub=price_rub,
            id_payment=payment.id,
        ),
    )
    await state.set_state(PaymentState.premium)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
