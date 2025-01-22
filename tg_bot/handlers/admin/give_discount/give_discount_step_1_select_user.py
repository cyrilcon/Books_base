from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, discounts_back_cancel_keyboard
from tg_bot.services.users import create_user_link, find_user
from tg_bot.states import GiveDiscount

give_discount_step_1_router = Router()


@give_discount_step_1_router.message(
    StateFilter(GiveDiscount.select_user),
    F.text,
)
async def give_discount_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    user, response_message = await find_user(l10n, message.text)

    if not user:
        await message.answer(response_message, reply_markup=cancel_keyboard(l10n))
        return

    if user.is_premium:
        await message.answer(
            l10n.format_value("give-discount-error-user-has-premium"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    discount_value = user.has_discount
    if discount_value:
        await message.answer(
            l10n.format_value(
                "give-discount-error-user-already-has-discount",
                {"discount_value": discount_value},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    id_user = user.id_user
    user_link = create_user_link(user.full_name, user.username)

    await message.answer(
        l10n.format_value(
            "give-discount-select-discount",
            {"user_link": user_link, "id_user": str(id_user)},
        ),
        reply_markup=discounts_back_cancel_keyboard(l10n),
    )
    await state.update_data(
        id_user_recipient=id_user,
        language_code_recipient=user.language_code,
        user_link=user_link,
    )
    await state.set_state(GiveDiscount.select_discount)
