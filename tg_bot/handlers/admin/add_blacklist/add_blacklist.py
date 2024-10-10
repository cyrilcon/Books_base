from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import AddBlacklist

command_add_blacklist_router = Router()


@command_add_blacklist_router.message(Command("add_blacklist"))
async def add_blacklist(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("add-blacklist"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBlacklist.select_user)
