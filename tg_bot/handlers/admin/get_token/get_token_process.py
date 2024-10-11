from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.states import GetToken

get_token_process_router = Router()


@get_token_process_router.message(
    StateFilter(GetToken.send_photo),
    F.photo,
)
async def get_token_process(
    message: Message,
    state: FSMContext,
):
    await message.answer(f"<code>{message.photo[-1].file_id}</code>")
    await state.clear()


@get_token_process_router.message(
    StateFilter(GetToken.send_photo),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def get_token_unprocessed_messages(
    message: Message,
    l10n: FluentLocalization,
):
    await message.answer(l10n.format_value("get-token-unprocessed-messages"))
