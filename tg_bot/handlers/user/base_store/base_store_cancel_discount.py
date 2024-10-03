from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import UserSchema
from tg_bot.config import config
from tg_bot.services import get_fluent_localization, create_user_link

base_store_cancel_discount_router = Router()


@base_store_cancel_discount_router.callback_query(F.data == "cancel_discount")
async def base_store_cancel_discount(
    call: CallbackQuery,
    l10n: FluentLocalization,
    user: UserSchema,
    bot: Bot,
):
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

    await api.users.discounts.delete_discount(id_user=user.id_user)
    await api.users.update_user(id_user=user.id_user, base_balance=base_balance)

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

    user_link = create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "base-store-cancel-discount-success-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "discount_value": discount_value,
                "base_balance": base_balance,
            },
        ),
    )
