from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import EditBook

command_edit_book_router = Router()


@command_edit_book_router.message(Command("edit_book"))
async def edit_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("edit-book"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(EditBook.select_book)
