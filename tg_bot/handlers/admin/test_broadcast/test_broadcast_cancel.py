from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.states import TestBroadcast

test_broadcast_cancel_router = Router()


@test_broadcast_cancel_router.callback_query(
    StateFilter(TestBroadcast),
    F.data == "cancel",
)
async def test_broadcast_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("test-broadcast-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
