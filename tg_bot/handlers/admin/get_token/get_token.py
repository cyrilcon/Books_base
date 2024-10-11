from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import GetToken

command_get_token_router = Router()


@command_get_token_router.message(Command("get_token"))
async def get_token(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("get-token"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GetToken.send_photo)
