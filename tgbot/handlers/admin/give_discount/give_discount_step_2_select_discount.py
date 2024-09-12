from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_localization
from tgbot.states import GiveDiscount

give_discount_step_2_router = Router()


@give_discount_step_2_router.callback_query(
    StateFilter(GiveDiscount.select_discount), F.data == "back"
)
async def back_to_give_discount_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("give-discount-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveDiscount.select_user)
    await call.answer()


@give_discount_step_2_router.callback_query(
    StateFilter(GiveDiscount.select_discount), F.data.startswith("discount")
)
async def give_discount_step_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    discount = int(call.data.split(":")[-2])

    data = await state.get_data()
    id_user_recipient = data["id_user_recipient"]
    user_link = data["user_link"]

    l10n_recipient = await get_user_localization(id_user_recipient)

    try:
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value(
                "give-discount-given",
                {"discount": discount},
            ),
            message_effect_id="5046509860389126442",
        )
    except AiogramError:
        await call.message.edit_text(l10n.format_value("error-user-blocked-bot"))
    else:
        await api.users.discounts.create_discount(
            id_user=id_user_recipient,
            discount=discount,
        )
        await call.message.edit_text(
            l10n.format_value(
                "give-discount-success",
                {
                    "discount": discount,
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                },
            )
        )
    await state.clear()
    await call.answer()
