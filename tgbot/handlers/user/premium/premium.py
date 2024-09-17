from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline.keyboards import pay_premium_keyboard
from tgbot.services import Payment

premium_router = Router()
premium_router.message.middleware(ChatActionMiddleware())


@premium_router.message(Command("premium"), flags={"chat_action": "typing"})
async def premium(message: Message, l10n: FluentLocalization):
    id_user = message.from_user.id
    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.is_premium:
        await message.answer(
            l10n.format_value("premium-error-user-already-has-premium")
        )
        return

    rub_price = 385
    stars_price = 200
    payment = Payment(amount=rub_price, comment="Books_base Premium")
    payment.create()
    url_payment = payment.invoice
    id_payment = payment.id

    await message.answer_invoice(
        title="Books_base Premium ⚜️",
        description=l10n.format_value(
            "premium", {"rub_price": rub_price, "stars_price": stars_price}
        ),
        prices=[LabeledPrice(label="XTR", amount=200)],
        provider_token="",
        payload="premium",
        currency="XTR",
        reply_markup=pay_premium_keyboard(
            l10n=l10n,
            url_payment=url_payment,
            price=rub_price,
            id_payment=id_payment,
        ),
    )
