from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import PaymentCurrencyEnum, PaymentTypeEnum, UserSchema
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import channel_keyboard
from tg_bot.services import Payment, create_user_link, get_fluent_localization
from tg_bot.states import Payment as PaymentState

payment_premium_router = Router()


@payment_premium_router.callback_query(
    StateFilter(PaymentState.premium),
    F.data.startswith("paid_premium"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def payment_premium(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
    bot: Bot,
):
    if user.is_premium:
        await call.message.edit_reply_markup()
        await call.answer(
            l10n.format_value("payment-premium-error-user-already-has-premium"),
            show_alert=True,
        )
        return

    id_payment = call.data.split(":")[-1]
    price = config.price.premium.rub

    if not Payment.check_payment(Payment(amount=price, id=id_payment)):
        await call.answer(
            l10n.format_value("payment-error-payment-not-found"),
            show_alert=True,
        )
        return

    await call.message.edit_reply_markup()

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user=user.id_user)

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=user.id_user,
        price=price,
        currency=PaymentCurrencyEnum.RUB,
        type=PaymentTypeEnum.PREMIUM,
    )

    await call.message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )
    await call.message.answer(
        l10n.format_value(
            "payment-premium-success",
            {"channel_link": config.channel.main_link},
        ),
        message_effect_id=MessageEffects.CONFETTI,
        reply_markup=channel_keyboard(l10n),
    )
    await state.clear()
    await call.answer()

    user_link = create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "payment-premium-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "price": price,
                "currency": "₽",
                "id_payment": id_payment,
            },
        ),
    )


@payment_premium_router.pre_checkout_query(StateFilter(PaymentState.premium))
async def payment_premium_on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    id_user = pre_checkout_query.from_user.id

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.is_blacklisted or user.is_premium:
        l10n = get_fluent_localization(user.language_code)
        await pre_checkout_query.answer(
            ok=False,
            error_message=l10n.format_value("payment-pre-checkout-failed-reason"),
        )

    await pre_checkout_query.answer(ok=True)


@payment_premium_router.message(
    StateFilter(PaymentState.premium),
    F.successful_payment,
)
async def payment_premium_on_successful(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
    bot: Bot,
):
    id_payment = message.successful_payment.telegram_payment_charge_id
    price = message.successful_payment.total_amount

    if user.has_discount:
        await api.users.discounts.delete_discount(id_user=user.id_user)

    await api.payments.create_payment(
        id_payment=id_payment,
        id_user=user.id_user,
        price=price,
        currency=PaymentCurrencyEnum.XTR,
        type=PaymentTypeEnum.PREMIUM,
    )

    await message.answer(
        l10n.format_value(
            "payment-check",
            {"id_payment": id_payment},
        ),
    )
    await message.answer(
        l10n.format_value(
            "payment-premium-success",
            {"channel_link": config.channel.main_link},
        ),
        message_effect_id=MessageEffects.CONFETTI,
        reply_markup=channel_keyboard(l10n),
    )
    await state.clear()

    user_link = create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "payment-premium-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "price": price,
                "currency": " ⭐️",
                "id_payment": id_payment,
            },
        ),
    )


@payment_premium_router.callback_query(
    StateFilter(PaymentState.premium),
    F.data == "cancel_payment",
)
async def payment_premium_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("payment-premium-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_reply_markup()


@payment_premium_router.message(
    StateFilter(PaymentState.premium),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def payment_premium_unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("payment-premium-unprocessed-messages"))
