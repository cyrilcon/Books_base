from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import Refund

command_refund_router = Router()


@command_refund_router.message(Command("refund"))
async def refund(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("refund"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Refund.select_payment)
