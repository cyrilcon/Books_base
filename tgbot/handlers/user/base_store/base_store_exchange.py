from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import discounts_keyboard

base_store_exchange_router = Router()


@base_store_exchange_router.callback_query(F.data == "exchange_base")
async def base_store_exchange_base(call: CallbackQuery, l10n: FluentLocalization):
    response = await api.users.get_user_by_id(call.from_user.id)
    user = response.get_model()

    if user.is_premium or user.has_discount:
        await call.answer(
            l10n.format_value("base-store-error-exchange-unavailable"),
            show_alert=True,
        )
        return

    await call.message.edit_text(
        l10n.format_value(
            "base-store-exchange-base",
            {"base_balance": user.base_balance},
        ),
        reply_markup=discounts_keyboard(l10n),
    )
    await call.answer()


@base_store_exchange_router.callback_query(F.data.startswith("discount"))
async def base_store_discount(call: CallbackQuery, l10n: FluentLocalization):
    discount = int(call.data.split(":")[-2])
    price = int(call.data.split(":")[-1])

    id_user = call.from_user.id

    response = await api.users.get_user_by_id(id_user)
    user = response.get_model()

    if user.is_premium or user.has_discount:
        await call.answer(
            l10n.format_value("base-store-error-exchange-unavailable"),
            show_alert=True,
        )
        return

    base_balance = user.base_balance - price

    if base_balance < 0:
        await call.answer(
            l10n.format_value("base-store-error-not-enough-base"),
            show_alert=True,
        )
        return

    await api.users.update_user(id_user=id_user, base_balance=base_balance)
    await api.users.discounts.create_discount(id_user=id_user, discount=discount)

    await call.message.edit_text(
        l10n.format_value(
            "base-store-exchange-success",
            {
                "price": price,
                "discount": discount,
                "base_balance": base_balance,
            },
        ),
    )
    await call.answer()
