from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.states import SendMessage

send_message_router_2 = Router()
send_message_router_2.message.filter(AdminFilter())


@send_message_router_2.callback_query(
    StateFilter(SendMessage.write_message), F.data == "back"
)
async def back_to_send_message_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("send-message-select-user"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendMessage.select_user)
