from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import TakeDiscount

command_take_discount_router = Router()


@command_take_discount_router.message(Command("take_discount"))
async def take_discount(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("take-discount"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TakeDiscount.select_user)
