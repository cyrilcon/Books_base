from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import AddAdmin

command_add_admin_router = Router()


@command_add_admin_router.message(Command("add_admin"))
async def add_admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("add-admin"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddAdmin.select_user)
