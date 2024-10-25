from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    yes_cancel_keyboard,
    edit_book_keyboard,
)
from tg_bot.services import generate_book_caption, BookFormatter
from tg_bot.states import EditBook

edit_title_router = Router()


@edit_title_router.callback_query(
    F.data.startswith("edit_title"),
    flags={"skip_message": 1},
)
async def edit_title(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book_by_id(id_book=id_book)
    book = response.get_model()

    await call.message.answer(
        l10n.format_value(
            "edit-book-title",
            {"title": book.title},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(id_book_edited=id_book)
    await state.set_state(EditBook.edit_title)
    await call.answer()


@edit_title_router.message(
    StateFilter(EditBook.edit_title),
    F.text,
)
async def edit_title_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    title = message.text

    if len(title) > 255:
        await message.answer(
            l10n.format_value("edit-book-error-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    if '"' in title:
        await message.answer(
            l10n.format_value("edit-book-error-invalid-title"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await state.update_data(title=title)

    response = await api.books.search_books_by_title(
        title=title,
        similarity_threshold=100,
    )
    result = response.get_model()

    if result.found > 0:
        book = result.books[0].book
        article = BookFormatter.format_article(book.id_book)

        await message.answer(
            l10n.format_value(
                "edit-book-error-title-already-exists",
                {"title": book.title, "article": article},
            ),
            reply_markup=yes_cancel_keyboard(l10n),
        )
        return

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, title=title)
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

    await api.books.update_book(id_book_edited=id_book_edited, title=title)

    await message.answer(l10n.format_value("edit-book-success"))
    await message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=book.id_book),
    )
    await state.clear()


@edit_title_router.callback_query(
    StateFilter(EditBook.edit_title),
    F.data == "yes",
)
async def edit_title_yes(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_reply_markup()

    data = await state.get_data()
    id_book_edited = data.get("id_book_edited")
    title = data.get("title")

    response = await api.books.get_book_by_id(id_book=id_book_edited)
    book = response.get_model()

    caption = await generate_book_caption(book_data=book, l10n=l10n, title=title)
    caption_length = len(caption)

    if caption_length > 1024:
        await call.message.answer(
            l10n.format_value(
                "edit-book-error-caption-too-long",
                {"caption_length": caption_length},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await api.books.update_book(id_book_edited=id_book_edited, title=title)

    await call.message.edit_text(l10n.format_value("edit-book-success"))
    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=edit_book_keyboard(l10n, id_book=book.id_book),
    )
    await state.clear()
    await call.answer()
