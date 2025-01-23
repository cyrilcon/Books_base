from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services.data import BookFormatter
from tg_bot.states import AddBook

command_add_book_router = Router()


@command_add_book_router.message(Command("add_book"))
async def add_book(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    response = await api.books.get_latest_article()
    latest_article = response.result

    free_article = BookFormatter.format_article(latest_article + 1)

    await message.answer(
        l10n.format_value(
            "add-book-article",
            {"free_article": free_article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(free_article=free_article)
    await state.set_state(AddBook.select_article)
