from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import GiveBook

command_give_book_router = Router()


@command_give_book_router.message(Command("give_book"))
async def give_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("give-book"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(GiveBook.select_user)
