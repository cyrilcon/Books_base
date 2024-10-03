from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.services import ClearKeyboard, get_fluent_localization, create_user_link
from .keyboards import discounts_keyboard, cancel_discount_keyboard

base_store_router = Router()


@base_store_router.message(Command("base_store"))
async def base_store(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    response = await api.users.get_user_by_id(id_user=message.from_user.id)
    user = response.get_model()

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


@base_store_router.callback_query(F.data.startswith("discount"))
async def base_store_discount(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    discount_value = int(call.data.split(":")[-2])
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

    await ClearKeyboard.clear(call, storage)
    await state.clear()
    await call.message.edit_reply_markup()

    await api.users.update_user(id_user=id_user, base_balance=base_balance)
    await api.users.discounts.create_discount(
        id_user=id_user,
        discount_value=discount_value,
    )

    await call.message.answer(
        l10n.format_value(
            "base-store-exchange-success",
            {
                "price": price,
                "discount_value": discount_value,
                "base_balance": base_balance,
            },
        ),
        message_effect_id=MessageEffects.CONFETTI,
        reply_markup=cancel_discount_keyboard(l10n, discount_value=discount_value),
    )
    await call.answer()

    user_link = create_user_link(user.full_name, user.username)

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(
            "base-store-exchange-success-message-for-admin",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "price": price,
                "discount_value": discount_value,
                "base_balance": base_balance,
            },
        ),
    )
