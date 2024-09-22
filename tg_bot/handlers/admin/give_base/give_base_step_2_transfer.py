from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.enums import MessageEffect
from tg_bot.api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import ClearKeyboard, get_user_localization
from tg_bot.states import GiveBase

give_base_step_2_router = Router()


@give_base_step_2_router.callback_query(
    StateFilter(GiveBase.transfer), F.data == "back"
)
async def back_to_give_base_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("give-base-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBase.select_user)
    await call.answer()


@give_base_step_2_router.message(StateFilter(GiveBase.transfer), F.text)
async def give_base_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    base_received = message.text

    if not base_received.isdigit() or int(base_received) <= 0:
        sent_message = await message.answer(
            l10n.format_value("give-base-error-invalid-base"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    base_received = int(base_received)

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    user_link = data.get("user_link")

    l10n_recipient = await get_user_localization(id_user_recipient)

    response = await api.users.get_user_by_id(id_user_recipient)
    user = response.get_model()

    base_balance = user.base_balance + base_received

    try:
        await bot.send_message(
            chat_id=id_user_recipient,
            text=l10n_recipient.format_value(
                "give-base-received",
                {"base_received": base_received, "base_balance": base_balance},
            ),
            message_effect_id=MessageEffect.CONFETTI,
        )
    except AiogramError:
        await message.answer(
            l10n.format_value("error-user-blocked-bot"),
        )
    else:
        await api.users.update_user(id_user_recipient, base_balance=base_balance)
        await message.answer(
            l10n.format_value(
                "give-base-success",
                {
                    "base_received": base_received,
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                    "base_balance": base_balance,
                },
            )
        )
    await state.clear()
