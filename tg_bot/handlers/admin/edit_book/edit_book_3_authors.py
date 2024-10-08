from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, edit_book_keyboard
from tg_bot.services import generate_book_caption, BookFormatter
from tg_bot.states import EditBook

edit_authors_router = Router()


@edit_authors_router.callback_query(
    F.data.startswith("edit_authors"),
    flags={"skip_message": 1},
)
async def edit_authors(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    authors = BookFormatter.format_authors(book.authors)

    await call.message.answer(
        l10n.format_value(
            "edit-book-authors",
            {"authors": authors},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_authors)
    await call.answer()


@edit_authors_router.message(
    StateFilter(EditBook.edit_authors),
    F.text,
)
async def edit_authors_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    authors = message.text.split(", ")

    for author_name in authors:
        if len(author_name) > 255:
            await message.answer(
                l10n.format_value("edit-book-error-author-name-too-long"),
                reply_markup=cancel_keyboard(l10n),
            )
            return

        if '"' in author_name:
            await message.answer(
                l10n.format_value("edit-book-error-invalid-author-name"),
                reply_markup=cancel_keyboard(l10n),
            )
            return

    authors = [{"author_name": author_name} for author_name in authors]

    data = await state.get_data()
    id_book_edited = data.get("id_edit_book")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, authors=authors)
    caption_length = len(caption)

    if caption_length > 1024:
        await message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await api.books.update_book(id_book_edited=id_book_edited, authors=authors)

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=book.id_book),
    )
    await state.clear()
