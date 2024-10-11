from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import TestBroadcast

command_test_broadcast_router = Router()


@command_test_broadcast_router.message(Command("test_broadcast"))
async def test_broadcast(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("test-broadcast"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(TestBroadcast.write_message)
