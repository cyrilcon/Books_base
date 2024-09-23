from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.api.books_base_api import api
from tg_bot.config import config

base_store_cancel_discount_router = Router()


@base_store_cancel_discount_router.callback_query(F.data == "cancel_discount")
async def base_store_cancel_discount(call: CallbackQuery, l10n: FluentLocalization):
    id_user = call.from_user.id

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()
    discount_value = user.has_discount

    if not discount_value:
        await call.answer(
            l10n.format_value("base-store-cancel-discount-error"),
            show_alert=True,
        )
        return

    discount_values = {
        15: config.price.discount.discount_15,
        30: config.price.discount.discount_30,
        50: config.price.discount.discount_50,
        100: config.price.discount.discount_100,
    }

    base_balance = user.base_balance + discount_values.get(discount_value)

    await api.users.discounts.delete_discount(id_user=id_user)
    await api.users.update_user(id_user=id_user, base_balance=base_balance)

    await call.message.edit_text(
        l10n.format_value(
            "base-store-cancel-discount-success",
            {
                "discount_value": discount_value,
                "base_balance": base_balance,
            },
        ),
    )
    await call.answer()
