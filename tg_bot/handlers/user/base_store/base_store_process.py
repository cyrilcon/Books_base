from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import UserSchema
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_discount_keyboard
from tg_bot.services import get_fluent_localization, create_user_link

base_store_process_router = Router()


@base_store_process_router.callback_query(F.data.startswith("discount"))
async def base_store_discount(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
    bot: Bot,
):
    discount_value = int(call.data.split(":")[-2])
    price = int(call.data.split(":")[-1])

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

    await state.clear()
    await call.message.edit_reply_markup()

    await api.users.update_user(id_user=user.id_user, base_balance=base_balance)
    await api.users.discounts.create_discount(
        id_user=user.id_user,
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
                "id_user": str(user.id_user),
                "price": price,
                "discount_value": discount_value,
                "base_balance": base_balance,
            },
        ),
    )
