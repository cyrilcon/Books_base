import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.enums import SearchBy
from tg_bot.services import BookFormatter, ClearKeyboard
from tg_bot.states import Search
from .keyboards import (
    search_by_keyboard,
    author_pagination_keyboard,
    author_book_pagination_keyboard,
)

search_by_author_router = Router()
search_by_author_router.message.middleware(ChatActionMiddleware())


@search_by_author_router.callback_query(F.data.startswith("search_by_author"))
async def search_by_author(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    await call.message.edit_text(
        l10n.format_value("search-by-author"),
        reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
    )
    await state.set_state(Search.by_author)
    await call.answer()


@search_by_author_router.message(
    StateFilter(Search.by_author),
    F.text,
    flags={"chat_action": "typing"},
)
async def search_by_author_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await author_search(message, l10n, state)


@search_by_author_router.callback_query(F.data.startswith("author_page"))
async def author_page(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    page = int(call.data.split(":")[-1])
    author_name_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await author_search(call.message, l10n, state, page, author_name_request)
    await call.answer()


@search_by_author_router.callback_query(F.data.startswith("get_author"))
async def get_author(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
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

    response = await api.books.get_books_by_author_id(id_author)
    result = response.get_model()
    count = result.count
    books = result.books

    text = l10n.format_value(
        "search-by-author-all-books",
        {"author_name": author.author_name},
    )
    book_number = 1

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
        text=text,
        reply_markup=author_book_pagination_keyboard(
            l10n=l10n,
            found=count,
            books=books,
            id_author=id_author,
        ),
    )
    await state.clear()
    await call.answer()


@search_by_author_router.callback_query(F.data.startswith("author_book_page"))
async def author_book_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-2])
    id_author = int(call.data.split(":")[-1])

    response = await api.books.get_books_by_author_id(id_author, page=page)
    result = response.get_model()
    found = result.count
    books = result.books

    author_name_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    text = l10n.format_value(
        "search-by-author-all-books",
        {"author_name": author_name_request},
    )
    book_number = ((page - 1) * 5) + 1

    for book in books:
        book = book.book

        article = BookFormatter.format_article(book.id_book)
        title = book.title
        authors = BookFormatter.format_authors(book.authors)

        text += (
            f"\n\n<b>{book_number}.</b> <code>{title}</code>\n"
            f"(<code>{article}</code>)"
        )
        book_number += 1

    await call.message.edit_text(
        text=text,
        reply_markup=author_book_pagination_keyboard(
            l10n=l10n,
            found=found,
            books=books,
            id_author=id_author,
            page=page,
        ),
    )
    await call.answer()


async def author_search(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    page: int = 1,
    author_name_request: str = None,
):
    """
    A common function for handling author searches and forward/backward button presses.
    :param message: Message or callback object.
    :param l10n: Language set by the user.
    :param state: Search state.
    :param page: Page number for pagination.
    :param author_name_request: Name of the author to search for.
    """

    if author_name_request is None:
        author_name_request = message.text

    author_name_request = author_name_request.replace('"', "")

    if len(author_name_request) > 255:
        await message.answer(
            l10n.format_value("search-by-author-error-author-name-too-long"),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
        )
        return

    response = await api.authors.search_authors(author_name_request, page=page)
    result = response.get_model()
    found = result.found
    authors = result.authors

    if found == 0:
        await message.answer(
            l10n.format_value(
                "search-by-author-error-not-found",
                {"author_name_request": author_name_request},
            ),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
        )
        return

    if found == 1:
        author = authors[0].author
        id_author = author.id_author

        response = await api.books.get_books_by_author_id(id_author)
        result = response.get_model()
        count = result.count
        books = result.books

        text = l10n.format_value(
            "search-by-author-all-books",
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
                text=text,
                reply_markup=author_book_pagination_keyboard(
                    l10n=l10n,
                    found=count,
                    books=books,
                    id_author=id_author,
                    page=page,
                ),
            )
        except TelegramBadRequest:
            await message.answer(
                text=text,
                reply_markup=author_book_pagination_keyboard(
                    l10n=l10n,
                    found=count,
                    books=books,
                    id_author=id_author,
                    page=page,
                ),
            )
        await state.clear()
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
            text=text,
            reply_markup=author_pagination_keyboard(
                l10n=l10n,
                found=found,
                authors=authors,
                page=page,
            ),
        )
    except TelegramBadRequest:
        await message.answer(
            text=text,
            reply_markup=author_pagination_keyboard(
                l10n=l10n,
                found=found,
                authors=authors,
                page=page,
            ),
        )
