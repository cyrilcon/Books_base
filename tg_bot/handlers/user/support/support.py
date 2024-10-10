from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import Support

command_support_router = Router()


@command_support_router.message(Command("support"))
async def support(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("support"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(reply_from_button=False)
    await state.set_state(Support.reply_to_admin)
