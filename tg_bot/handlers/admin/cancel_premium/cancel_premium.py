from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import CancelPremium

command_cancel_premium_router = Router()


@command_cancel_premium_router.message(Command("cancel_premium"))
async def cancel_premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("cancel-premium"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(CancelPremium.select_user)
