import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.enums import SearchBy
from tgbot.keyboards.inline import search_by_keyboard, book_pagination_keyboard
from tgbot.services import generate_book_caption, BookFormatter

search_by_title_router = Router()
search_by_title_router.message.middleware(ChatActionMiddleware())


@search_by_title_router.callback_query(F.data.startswith("search_by_title"))
async def search_by_title(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("search-by-title"),
        reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
    )
    await state.clear()
    await call.answer()


@search_by_title_router.message(F.text, flags={"chat_action": "typing"})
async def search_by_title_process(message: Message, l10n: FluentLocalization):
    await book_search(message, l10n)


@search_by_title_router.callback_query(F.data.startswith("book_page"))
async def book_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-1])
    book_title_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await book_search(call.message, l10n, page, book_title_request)
    await call.answer()


@search_by_title_router.callback_query(F.data.startswith("get_book"))
async def get_book(call: CallbackQuery, l10n: FluentLocalization):
    id_book = int(call.data.split(":")[-1])
    article = BookFormatter.format_article(id_book)

    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status != 200:
        await call.message.answer(
            l10n.format_value(
                "search-by-title-error-book-unavailable",
                {"article": article},
            )
        )
        await call.answer()
        return

    book = response.get_model()
    caption = await generate_book_caption(book_data=book, l10n=l10n)

    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
    )
    await call.answer()


async def book_search(
    message: Message,
    l10n: FluentLocalization,
    page: int = 1,
    book_title_request: str = None,
):
    """
    A common function for handling book searches and forward/backward button presses.
    :param message: Message or callback object.
    :param l10n: Language set by the user.
    :param page: Page number for pagination.
    :param book_title_request: Title of the book to search for.
    """

    if book_title_request is None:
        book_title_request = message.text

    book_title_request = book_title_request.replace('"', "")

    if len(book_title_request) > 255:
        await message.answer(
            l10n.format_value("search-by-title-error-title-too-long"),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
        )
        return

    response = await api.books.search_books_by_title(book_title_request, page=page)
    result = response.get_model()
    found = result.found
    books = result.books

    if found == 0:
        await message.answer(
            l10n.format_value(
                "search-by-title-not-found",
                {"book_title_request": book_title_request},
            ),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
        )
        return

    if found == 1:
        book = books[0].book
        caption = await generate_book_caption(book_data=book, l10n=l10n)

        await message.answer_photo(
            photo=book.cover,
            caption=caption,
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
        return

    text = l10n.format_value(
        "search-by-title-success",
        {"book_title_request": book_title_request},
    )
    book_number = ((page - 1) * 5) + 1

    for book in books:
        book = book.book

        article = BookFormatter.format_article(book.id_book)
        title = book.title
        authors = BookFormatter.format_authors(book.authors)

        text += (
            f"\n\n<b>{book_number}.</b> <code>{title}</code>\n"
            f"<i>{authors}</i> (<code>{article}</code>)"
        )
        book_number += 1
    try:
        await message.edit_text(
            text,
            reply_markup=book_pagination_keyboard(
                l10n=l10n,
                found=found,
                books=books,
                page=page,
            ),
        )
    except TelegramBadRequest:
        await message.answer(
            text,
            reply_markup=book_pagination_keyboard(
                l10n=l10n,
                found=found,
                books=books,
                page=page,
            ),
        )
