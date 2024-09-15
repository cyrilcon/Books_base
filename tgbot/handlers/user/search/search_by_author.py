import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.enums import SearchBy
from tgbot.keyboards.inline import (
    search_by_keyboard,
    author_search_pagination_keyboard,
    book_pagination_keyboard,
)
from tgbot.services import BookFormatter
from tgbot.states import AuthorSearch

search_by_author_router = Router()
search_by_author_router.message.middleware(ChatActionMiddleware())


@search_by_author_router.callback_query(F.data.startswith("search_by_author"))
async def search_by_author(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.message.edit_text(
        l10n.format_value("search-by-author"),
        reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
    )
    await state.set_state(AuthorSearch.select_author)
    await call.answer()


@search_by_author_router.message(
    StateFilter(AuthorSearch.select_author),
    F.text,
    flags={"chat_action": "typing"},
)
async def search_by_author_process(message: Message, l10n: FluentLocalization):
    await author_search(message, l10n)


@search_by_author_router.callback_query(F.data.startswith("author_search_page"))
async def book_search_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-1])
    author_name_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await author_search(call.message, l10n, page, author_name_request)
    await call.answer()


@search_by_author_router.callback_query(F.data.startswith("get_author"))
async def search_get_author(call: CallbackQuery, l10n: FluentLocalization):
    id_author = int(call.data.split(":")[-1])

    response = await api.authors.get_author_by_id(id_author)
    status = response.status

    if status != 200:
        await call.message.answer(
            l10n.format_value("search-by-author-error-author-unavailable")
        )
        await call.answer()
        return

    author = response.get_model()
    response = await api.books.get_books_by_author_id(author.id_author)
    result = response.get_model()
    count = result.count
    books = result.books

    page = 1

    text = l10n.format_value(
        "search-by-author-success-books",
        {"author_name": author.author_name},
    )
    book_number = ((page - 1) * 5) + 1

    for book in books:
        book = book.book
        article = BookFormatter.format_article(book.id_book)
        title = book.title
        text += (
            f"\n\n<b>{book_number}.</b> <code>{title}</code>\n"
            f"(<code>{article}</code>)"
        )
        book_number += 1

    await call.message.edit_text(
        text,
        reply_markup=book_pagination_keyboard(l10n, count, books, page),
    )  # TODO: кнопки book_author_page
    # TODO: Выйти из состояния
    await call.answer()


async def author_search(
    message: Message,
    l10n: FluentLocalization,
    page: int = 1,
    author_name_request: str = None,
):
    """
    A common function for handling book searches and forward/backward button presses.
    :param message: Message or callback object.
    :param l10n: Language set by the user.
    :param page: Page number for pagination.
    :param author_name_request: Title of the book to search for.
    """

    if author_name_request is None:
        author_name_request = message.text

    if len(author_name_request) > 255:
        await message.answer(
            l10n.format_value("search-by-author-error-name-too-long"),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
        )
        return

    response = await api.authors.search_authors(author_name_request, page=page)
    result = response.get_model()
    found = result.found
    authors = result.authors

    if found == 0:
        await message.answer(
            l10n.format_value("search-not-found", {"request": author_name_request}),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
        )
        return

    if found == 1:
        author = authors[0].author
        response = await api.books.get_books_by_author_id(author.id_author)
        result = response.get_model()
        books = result.books

        text = l10n.format_value(
            "search-by-author-success-books",
            {"author_name": author.author_name},
        )
        book_number = ((page - 1) * 5) + 1

        for book in books:
            book = book.book
            article = BookFormatter.format_article(book.id_book)
            title = book.title
            text += (
                f"\n\n<b>{book_number}.</b> <code>{title}</code>\n"
                f"(<code>{article}</code>)"
            )
            book_number += 1
        try:
            await message.edit_text(
                text,
                reply_markup=book_pagination_keyboard(l10n, found, books, page),
            )
        except TelegramBadRequest:
            await message.answer(
                text,
                reply_markup=book_pagination_keyboard(l10n, found, books, page),
            )
        return

    text = l10n.format_value(
        "search-by-author-success",
        {"author_name_request": author_name_request},
    )
    author_number = ((page - 1) * 5) + 1

    for author in authors:
        author = author.author
        author_name = author.author_name
        text += f"\n\n<b>{author_number}.</b> <code>{author_name}</code>"
        author_number += 1
    try:
        await message.edit_text(
            text,
            reply_markup=author_search_pagination_keyboard(l10n, found, authors, page),
        )
    except TelegramBadRequest:
        await message.answer(
            text,
            reply_markup=author_search_pagination_keyboard(l10n, found, authors, page),
        )
