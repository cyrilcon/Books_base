from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import exchange_base_keyboard
from tgbot.services import ClearKeyboard

base_store_router = Router()


@base_store_router.message(Command("base_store"))
async def base_store(
    message: Message,
    l10n: FluentLocalization,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    response = await api.users.get_user_by_id(message.from_user.id)
    user = response.get_model()

    if user.is_premium:
        account_information = l10n.format_value("base-store-user-has-premium")
        await message.answer(
            l10n.format_value(
                "base-store",
                {"account_information": account_information},
            )
        )
        return

    discount = user.has_discount
    if discount == 100:
        account_information = l10n.format_value("base-store-user-has-free-book")
        keyboard = None
    elif discount > 0:
        account_information = l10n.format_value(
            "base-store-user-has-discount",
            {"discount": discount},
        )
        keyboard = None
    else:
        account_information = l10n.format_value(
            "base-balance",
            {"base_balance": user.base_balance},
        )
        keyboard = exchange_base_keyboard(l10n)

    await message.answer(
        l10n.format_value(
            "base-store",
            {"account_information": account_information},
        ),
        reply_markup=keyboard,
    )
