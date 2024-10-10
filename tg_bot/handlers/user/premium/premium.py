from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LabeledPrice
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from api.books_base_api.schemas import UserSchema
from tg_bot.config import config
from tg_bot.keyboards.inline import pay_premium_keyboard
from tg_bot.services import Payment
from tg_bot.states import Payment as PaymentState

command_premium_router = Router()
command_premium_router.message.middleware(ChatActionMiddleware())


@command_premium_router.message(
    Command("premium"),
    flags={"chat_action": "typing"},
)
async def premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
):
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
            url_payment=payment.invoice,
            price_xtr=price_xtr,
            price_rub=price_rub,
            id_payment=payment.id,
        ),
    )
    await state.set_state(PaymentState.premium)
