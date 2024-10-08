from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import GiveBase

command_give_base_router = Router()


@command_give_base_router.message(Command("give_base"))
async def give_base(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("give-base"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBase.select_user)
