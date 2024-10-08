from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import TakeBase

command_take_base_router = Router()


@command_take_base_router.message(Command("take_base"))
async def take_base(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("take-base"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TakeBase.select_user)
