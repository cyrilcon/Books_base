from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.states import SendMessage

send_message_cancel_router = Router()


@send_message_cancel_router.callback_query(
    StateFilter(SendMessage),
    F.data == "cancel",
)
async def send_message_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("send-message-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
