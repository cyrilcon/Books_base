from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.states import Payment

premium_cancel_payment_router = Router()


@premium_cancel_payment_router.callback_query(
    StateFilter(Payment.premium),
    F.data == "cancel_payment",
)
async def premium_cancel_payment(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("premium-payment-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_reply_markup()
