from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.config import config
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import get_fluent_localization
from tg_bot.states import GiveDiscount

give_discount_step_2_router = Router()


@give_discount_step_2_router.callback_query(
    StateFilter(GiveDiscount.select_discount),
    F.data == "back",
)
async def back_to_give_discount_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("give-discount-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveDiscount.select_user)
    await call.answer()


@give_discount_step_2_router.callback_query(
    StateFilter(GiveDiscount.select_discount),
    F.data.startswith("discount"),
)
async def give_discount_step_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    discount_value = int(call.data.split(":")[-2])

    data = await state.get_data()
    id_user_recipient = data["id_user_recipient"]
    language_code_recipient = data["language_code_recipient"]
    user_link = data["user_link"]

    l10n_recipient = get_fluent_localization(language_code_recipient)
    try:
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value(
                "give-discount-success-message-for-user",
                {"discount_value": discount_value},
            ),
            message_effect_id=MessageEffects.CONFETTI,
        )
    except AiogramError:
        await call.message.edit_text(l10n.format_value("error-user-blocked-bot"))
    else:
        await api.users.discounts.create_discount(
            id_user=id_user_recipient,
            discount_value=discount_value,
        )

        l10n_params = {
            "msg_id": "give-discount-success",
            "args": {
                "discount_value": discount_value,
                "user_link": user_link,
                "id_user": str(id_user_recipient),
            },
        }

        await call.message.edit_text(
            l10n.format_value(
                msg_id=l10n_params["msg_id"],
                args=l10n_params["args"],
            )
        )

        l10n_chat = get_fluent_localization(config.chat.language_code)
        await bot.send_message(
            chat_id=config.chat.payment,
            text=l10n_chat.format_value(
                msg_id=l10n_params["msg_id"],
                args=l10n_params["args"],
            ),
        )
    await state.clear()
    await call.answer()
