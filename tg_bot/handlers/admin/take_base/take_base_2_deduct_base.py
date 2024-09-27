from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import ClearKeyboard, get_fluent_localization
from tg_bot.states import TakeBase

take_base_step_2_router = Router()


@take_base_step_2_router.callback_query(
    StateFilter(TakeBase.deduct_base),
    F.data == "back",
)
async def back_to_take_base_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("take-base-prompt-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TakeBase.select_user)
    await call.answer()


@take_base_step_2_router.message(
    StateFilter(TakeBase.deduct_base),
    F.text,
)
async def take_base_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    base_deducted = message.text

    if not base_deducted.isdigit() or int(base_deducted) == 0:
        sent_message = await message.answer(
            l10n.format_value("take-base-error-invalid-base"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    base_deducted = int(base_deducted)

    data = await state.get_data()
    id_user_recipient = data.get("id_user_recipient")
    user_link = data.get("user_link")

    response = await api.users.get_user_by_id(id_user_recipient)
    user = response.get_model()

    base_balance = user.base_balance

    base_balance = max(0, base_balance - base_deducted)

    await api.users.update_user(id_user=id_user_recipient, base_balance=base_balance)

    l10n_params = {
        "key": "take-base-success",
        "params": {
            "base_deducted": base_deducted,
            "user_link": user_link,
            "id_user": str(id_user_recipient),
            "base_balance": base_balance,
        },
    }

    await message.answer(l10n.format_value(l10n_params["key"], l10n_params["params"]))

    l10n_chat = get_fluent_localization(config.chat.language_code)
    await bot.send_message(
        chat_id=config.chat.payment,
        text=l10n_chat.format_value(l10n_params["key"], l10n_params["params"]),
    )
    await state.clear()
