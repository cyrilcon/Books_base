from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import GiveDiscount

command_give_discount_router = Router()


@command_give_discount_router.message(Command("give_discount"))
async def give_discount(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("give-discount"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveDiscount.select_user)
