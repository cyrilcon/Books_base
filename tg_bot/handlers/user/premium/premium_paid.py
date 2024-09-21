from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message
from fluent.runtime import FluentLocalization

from keyboards.inline import channel_keyboard
from services import get_user_localization, ClearKeyboard
from tg_bot.api.books_base_api import api
from tg_bot.config import config
from tg_bot.services import Payment, create_user_link
from tg_bot.states import Payment as PaymentState

premium_paid_router = Router()


@premium_paid_router.callback_query(
    StateFilter(PaymentState.premium),
    F.data.startswith("premium_paid"),
)
async def premium_paid(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    currency = call.data.split(":")[-3]
    price = float(call.data.split(":")[-2])
    id_payment = call.data.split(":")[-1]

    if not Payment.check_payment(Payment(amount=float(price), id=id_payment)):
        await call.message.answer(
            l10n.format_value("premium-paid-error-payment-not-found")
        )
        await call.answer()
        return

    await call.message.edit_reply_markup()

    id_user = call.from_user.id
    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user)

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=id_user,
        price=price,
        currency=currency,
        type="premium",
    )

    await call.message.answer(
        l10n.format_value(
            "premium-payment-successful",
            {
                "id_payment": id_payment,
                "channel_link": config.channel.link,
            },
        ),
        message_effect_id="5046509860389126442",
        reply_markup=channel_keyboard(l10n),
    )
    await state.clear()

    user_link = await create_user_link(user.full_name, user.username)

    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n.format_value(
            "premium-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "price": price,
                "currency": "₽",
                "id_payment": id_payment,
            },
        ),
    )


@premium_paid_router.pre_checkout_query(StateFilter(PaymentState.premium))
async def premium_on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    id_user = pre_checkout_query.from_user.id
    l10n = await get_user_localization(id_user)

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.is_blacklisted or user.is_premium:
        await pre_checkout_query.answer(
            ok=False,
            error_message=l10n.format_value("premium-pre-checkout-failed-reason"),
        )

    await pre_checkout_query.answer(ok=True)


@premium_paid_router.message(StateFilter(PaymentState.premium), F.successful_payment)
async def premium_on_successful_payment(
    message: Message,
    l10n: FluentLocalization,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    id_payment = message.successful_payment.telegram_payment_charge_id
    price = float(message.successful_payment.total_amount)

    id_user = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user)

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=id_user,
        price=price,
        currency="XTR",
        type="premium",
    )

    await message.answer(
        l10n.format_value(
            "premium-payment-check",
            {"id_payment": id_payment},
        ),
    )
    await message.answer(
        l10n.format_value(
            "premium-payment-successful",
            {"channel_link": config.channel.link},
        ),
        message_effect_id="5046509860389126442",
        reply_markup=channel_keyboard(l10n),
    )

    await bot.refund_star_payment(
        user_id=message.from_user.id,
        telegram_payment_charge_id=id_payment,
    )

    user_link = await create_user_link(full_name, username)

    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n.format_value(
            "premium-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "price": price,
                "currency": "⭐️",
                "id_payment": id_payment,
            },
        ),
    )
