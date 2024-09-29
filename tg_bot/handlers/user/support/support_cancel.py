from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.states import Support

support_cancel_router = Router()


@support_cancel_router.callback_query(
    StateFilter(Support),
    F.data == "cancel",
)
async def support_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    current_state = await state.get_state()

    if current_state.split(":")[-1] == "reply_to_user":
        text = l10n.format_value("support-admin-message-canceled")
    else:
        text = l10n.format_value("support-user-message-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
