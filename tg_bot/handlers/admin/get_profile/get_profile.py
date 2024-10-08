from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import GetProfile

command_get_profile_router = Router()


@command_get_profile_router.message(Command("get_profile"))
async def get_profile(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("get-profile"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GetProfile.select_user)
