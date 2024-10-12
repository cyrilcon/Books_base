from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api.schemas import UserSchema

command_my_account = Router()


@command_my_account.message(Command("my_account"))
async def my_account(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
):
    if user.is_premium:
        has_discount_or_premium = (
            "\n" + l10n.format_value("my-account-has-premium") + "\n"
        )
    elif user.has_discount:
        has_discount_or_premium = (
            "\n"
            + l10n.format_value(
                "my-account-has-discount",
                {"discount": user.has_discount},
            )
            + "\n"
        )
    else:
        has_discount_or_premium = ""

    await message.answer(
        l10n.format_value(
            "my-account",
            {
                "full_name": user.full_name,
                "has_discount_or_premium": has_discount_or_premium,
                "base_balance": user.base_balance,
            },
        )
    )
