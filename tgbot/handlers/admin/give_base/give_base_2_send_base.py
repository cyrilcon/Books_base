from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
)
from tgbot.services import (
    ClearKeyboard,
    Messenger,
    get_user_language,
)
from tgbot.states import GiveBase

give_base_router_2 = Router()
give_base_router_2.message.filter(AdminFilter())


@give_base_router_2.callback_query(StateFilter(GiveBase.send_base), F.data == "back")
async def back_to_give_base_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("give-base-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBase.select_user)


@give_base_router_2.message(StateFilter(GiveBase.send_base), F.text)
async def give_base_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(message, storage)

    base_received = message.text

    if base_received.isdigit() and int(base_received) > 0:
        base_received = int(base_received)

        data = await state.get_data()
        id_user_recipient = data.get("id_user_recipient")
        user_link = data.get("user_link")

        response = await api.users.get_user_by_id(id_user_recipient)
        user = response.result
        user_balance = user["base"] + base_received
        await api.users.update_user(id_user_recipient, base=user_balance)

        l10n_recipient = await get_user_language(id_user_recipient)

        id_sent = await Messenger.safe_send_message(
            bot=bot,
            user_id=id_user_recipient,
            text=l10n_recipient.format_value(
                "give-base-received",
                {"base_received": base_received, "user_balance": user_balance},
            ),
        )

        if id_sent:
            await message.answer(
                l10n.format_value(
                    "give-base-success",
                    {
                        "base_received": base_received,
                        "user_link": user_link,
                        "id_user": str(id_user_recipient),
                    },
                )
            )
        else:
            await message.answer(l10n.format_value("user-blocked-bot"))

        await state.clear()

    else:
        sent_message = await message.answer(
            l10n.format_value("give-base-incorrect"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
