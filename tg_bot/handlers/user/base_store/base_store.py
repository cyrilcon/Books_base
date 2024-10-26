from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from config import config
from api.api_v1.schemas import UserSchema
from tg_bot.keyboards.inline import cancel_discount_keyboard, discounts_keyboard

command_base_store_router = Router()


@command_base_store_router.message(
    Command("base_store"),
    flags={"safe_message": False},
)
async def base_store(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
):
    if user.is_premium:
        await message.answer(l10n.format_value("base-store-error-user-has-premium"))
        return

    discount_value = user.has_discount

    if discount_value:
        keyboard = cancel_discount_keyboard(l10n, discount_value=discount_value)
    else:
        keyboard = discounts_keyboard(l10n)

    await message.answer(
        l10n.format_value(
            "base-store",
            {
                "price_discount_15": config.price.discount.discount_15,
                "price_discount_30": config.price.discount.discount_30,
                "price_discount_50": config.price.discount.discount_50,
                "price_discount_100": config.price.discount.discount_100,
                "discount_value": discount_value,
                "base_balance": user.base_balance,
            },
        ),
        reply_markup=keyboard,
    )
