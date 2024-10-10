from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import SendBook

comment_send_book_router = Router()


@comment_send_book_router.message(Command("send_book"))
async def send_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("send-book"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(SendBook.select_user)
