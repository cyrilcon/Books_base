from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
)
from tgbot.services import (
    ClearKeyboard,
)
from tgbot.states import TakeBase

take_base_router_2 = Router()
take_base_router_2.message.filter(AdminFilter())


@take_base_router_2.callback_query(
    StateFilter(TakeBase.take_away_base), F.data == "back"
)
async def back_to_take_base_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("take-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TakeBase.select_user)


@take_base_router_2.message(StateFilter(TakeBase.take_away_base), F.text)
async def take_base_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    base_taken = message.text

    if base_taken.isdigit() and int(base_taken) != 0:
        base_taken = int(base_taken)

        data = await state.get_data()
        id_user_recipient = data.get("id_user_recipient")
        user_link = data.get("user_link")

        response = await api.users.get_user_by_id(id_user_recipient)
        user = response.result
        current_balance = user["base"]

        new_balance = max(0, current_balance - base_taken)

        await api.users.update_user(id_user_recipient, base=new_balance)

        await message.answer(
            l10n.format_value(
                "take-base-success",
                {
                    "base_taken": base_taken,
                    "user_link": user_link,
                    "id_user": str(id_user_recipient),
                    "user_balance": new_balance,
                },
            )
        )

        await state.clear()

    else:
        sent_message = await message.answer(
            l10n.format_value("base-incorrect"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
