from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import GivePremium

command_give_premium_router = Router()


@command_give_premium_router.message(Command("give_premium"))
async def give_premium(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("give-premium"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GivePremium.select_user)
