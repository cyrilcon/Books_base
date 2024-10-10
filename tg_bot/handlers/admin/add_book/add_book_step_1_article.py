from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import is_valid_book_article
from tg_bot.states import AddBook

add_book_step_1_router = Router()


@add_book_step_1_router.message(
    StateFilter(AddBook.select_article),
    F.text,
)
async def add_book_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    article = message.text

    data = await state.get_data()
    free_article = data.get("free_article")

    if not is_valid_book_article(article):
        await message.answer(
            l10n.format_value(
                "add-book-error-invalid-article",
                {"free_article": free_article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status == 200:
        await message.answer(
            l10n.format_value(
                "add-book-error-article-already-exists",
                {"free_article": free_article},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await message.answer(
        l10n.format_value("add-book-title"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(id_book=id_book)
    await state.set_state(AddBook.add_title)
