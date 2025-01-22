from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.enums import MessageEffects
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services.localization import get_fluent_localization
from tg_bot.states import GiveBase

give_base_step_2_router = Router()


@give_base_step_2_router.callback_query(
    StateFilter(GiveBase.transfer_base),
    F.data == "back",
)
async def back_to_give_base_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("give-base"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBase.select_user)
    await call.answer()


@give_base_step_2_router.message(
    StateFilter(GiveBase.transfer_base),
    F.text,
)
async def give_base_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    base_received = message.text

    if not base_received.isdigit() or int(base_received) <= 0:
        await message.answer(
            l10n.format_value("give-base-error-invalid-base"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    base_received = int(base_received)

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    user_link = data.get("user_link")

    response = await api.users.get_user_by_id(id_user=id_user_recipient)
    user = response.get_model()

    base_balance = user.base_balance + base_received

    l10n_recipient = get_fluent_localization(user.language_code)
    try:
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value(
                "give-base-success-message-for-user",
                {"base_received": base_received, "base_balance": base_balance},
            ),
            message_effect_id=MessageEffects.CONFETTI,
        )
    except AiogramError:
        await message.answer(
            l10n.format_value("error-user-blocked-bot"),
        )
    else:
        await api.users.update_user(
            id_user=id_user_recipient,
            base_balance=base_balance,
        )

        l10n_params = {
            "msg_id": "give-base-success",
            "args": {
                "base_received": base_received,
                "user_link": user_link,
                "id_user": str(id_user_recipient),
                "base_balance": base_balance,
            },
        }

        await message.answer(
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
