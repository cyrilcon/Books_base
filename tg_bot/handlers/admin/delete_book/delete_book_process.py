from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import is_valid_book_article
from tg_bot.states import DeleteBook

delete_book_process_router = Router()


@delete_book_process_router.message(
    StateFilter(DeleteBook.select_book),
    F.text,
)
async def delete_book_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    article = message.text

    if not is_valid_book_article(article):
        await message.answer(
            l10n.format_value("delete-book-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    id_book = int(article.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book)
    status = response.status

    if status != 200:
        await message.answer(
            l10n.format_value("delete-book-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    book = response.get_model()
    await api.books.delete_book(id_book=id_book)

    await message.answer(
        l10n.format_value(
            "delete-book-success",
            {"title": book.title},
        )
    )
    await state.clear()
