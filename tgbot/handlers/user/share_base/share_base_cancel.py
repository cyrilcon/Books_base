from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.states import ShareBase

share_base_cancel_router = Router()


@share_base_cancel_router.callback_query(F.data == "share_base_cancel")
@share_base_cancel_router.callback_query(StateFilter(ShareBase), F.data == "cancel")
async def share_base_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):

    text = l10n.format_value("share-base-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    try:
        await call.message.edit_text(text)
    except TelegramBadRequest:
        await call.message.edit_reply_markup()
