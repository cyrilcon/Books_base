from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import RemoveAdmin

command_remove_admin_router = Router()


@command_remove_admin_router.message(Command("remove_admin"))
async def remove_admin(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("remove-admin"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(RemoveAdmin.select_admin)
