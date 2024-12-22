from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, LabeledPrice
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from config import config
from api.api_v1.schemas import UserSchema
from tg_bot.keyboards.inline import pay_premium_keyboard
from tg_bot.services import Payment, ClearKeyboard
from tg_bot.states import Payment as PaymentState

command_premium_router = Router()
command_premium_router.message.middleware(ChatActionMiddleware())


@command_premium_router.message(
    Command("premium"),
    flags={
        "chat_action": "typing",
        "clear_keyboard": False,
        "throttle": True,
    },
)
async def premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    user: UserSchema,
):
    await ClearKeyboard.clear(message, storage)

    if user.is_premium:
        await message.answer(
            l10n.format_value("payment-premium-error-user-already-has-premium")
        )
        return

    price_rub = config.price.premium.rub
    price_xtr = config.price.premium.xtr

    payment = Payment(
        amount=price_rub,
        comment=l10n.format_value("Books_base Premium"),
    )
    payment.create()
    payment_link = await payment.invoice()

    await message.answer_invoice(
        title="Books_base Premium ⚜️",
        description=l10n.format_value(
            "payment-premium",
            {"price_rub": price_rub, "price_xtr": price_xtr},
        ),
        prices=[LabeledPrice(label="XTR", amount=price_xtr)],
        provider_token="",
        payload="premium",
        currency="XTR",
        reply_markup=pay_premium_keyboard(
            l10n=l10n,
            url_payment=payment_link,
            price_xtr=price_xtr,
            price_rub=price_rub,
            id_payment=payment.id,
        ),
    )
    await state.set_state(PaymentState.premium)
