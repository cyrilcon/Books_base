from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import Broadcast

command_broadcast_router = Router()


@command_broadcast_router.message(Command("broadcast"))
async def broadcast(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("broadcast"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Broadcast.write_message)
