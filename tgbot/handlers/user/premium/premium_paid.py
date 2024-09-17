from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from keyboards.inline import channel_keyboard
from tgbot.api.books_base_api import api
from tgbot.config import config
from tgbot.services import Payment, create_user_link

premium_paid_router = Router()


@premium_paid_router.callback_query(F.data.startswith("premium_paid"))
async def premium_paid(
    call: CallbackQuery,
    l10n: FluentLocalization,
    bot: Bot,
):
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

    await api.users.premium.create_premium(id_user)
    # TODO: add payment to db

    await call.message.answer(
        l10n.format_value(
            "premium-paid-success",
            {"channel_link": config.channel.link},
        ),
        message_effect_id="5046509860389126442",
        reply_markup=channel_keyboard(l10n),
    )

    user_link = await create_user_link(user.full_name, user.username)

    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n.format_value(
            "premium-paid-message-for-admin",
            {
                "user_link": user_link,
                "id_user": int(id_user),
                "price": price,
                "currency": "₽",
                "id_payment": id_payment,
            },
        ),
    )
