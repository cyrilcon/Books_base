from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.states import RemoveAdmin

remove_admin_cancel_router = Router()


@remove_admin_cancel_router.callback_query(
    StateFilter(RemoveAdmin),
    F.data == "cancel",
)
async def remove_admin_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("remove-admin-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
