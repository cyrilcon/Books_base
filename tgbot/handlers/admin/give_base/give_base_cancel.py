from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.states import GiveBase

give_base_cancel_router = Router()


@give_base_cancel_router.callback_query(StateFilter(GiveBase), F.data == "cancel")
async def give_base_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("give-base-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
