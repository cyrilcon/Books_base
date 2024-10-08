from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import DeleteBook

command_delete_book_router = Router()


@command_delete_book_router.message(Command("delete_book"))
async def delete_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("delete-book"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(DeleteBook.select_book)
