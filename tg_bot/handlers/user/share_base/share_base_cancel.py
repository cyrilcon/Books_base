from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.states import ShareBase

share_base_cancel_router = Router()


@share_base_cancel_router.callback_query(F.data == "share_base_cancel")
@share_base_cancel_router.callback_query(StateFilter(ShareBase), F.data == "cancel")
async def share_base_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("share-base-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
