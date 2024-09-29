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
    genre_pagination_keyboard,
    genre_book_pagination_keyboard,
    genres_pagination_keyboard,
)

search_by_genre_router = Router()
search_by_genre_router.message.middleware(ChatActionMiddleware())


@search_by_genre_router.callback_query(F.data.startswith("search_by_genre"))
async def search_by_genre(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    response = await api.genres.get_genres_with_pagination()
    genres = response.get_model()

    text = l10n.format_value("search-by-genre")
    genre_number = 1

    response = await api.genres.get_genres_count()
    genres_count = response.result

    for genre in genres:
        text += f"\n\n<b>{genre_number}.</b> <code>{genre.genre_name}</code>\n"
        genre_number += 1

    await call.message.edit_text(
        text=text,
        reply_markup=genres_pagination_keyboard(
            l10n=l10n,
            genres=genres,
            found=genres_count,
        ),
    )
    await state.set_state(Search.by_genre)
    await call.answer()


@search_by_genre_router.message(
    StateFilter(Search.by_genre),
    F.text,
    flags={"chat_action": "typing"},
)
async def search_by_genre_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await genre_search(message, l10n, state)


@search_by_genre_router.callback_query(F.data.startswith("genres_page"))
async def genres_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-1])

    response = await api.genres.get_genres_with_pagination(page=page)
    genres = response.get_model()

    text = l10n.format_value("search-by-genre")
    genre_number = ((page - 1) * 5) + 1

    response = await api.genres.get_genres_count()
    genres_count = response.result

    for genre in genres:
        text += f"\n\n<b>{genre_number}.</b> <code>{genre.genre_name}</code>\n"
        genre_number += 1

    await call.message.edit_text(
        text=text,
        reply_markup=genres_pagination_keyboard(
            l10n=l10n,
            genres=genres,
            found=genres_count,
            page=page,
        ),
    )
    await call.answer()


@search_by_genre_router.callback_query(F.data.startswith("genre_page"))
async def genre_page(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    page = int(call.data.split(":")[-1])
    genre_name_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await genre_search(call.message, l10n, state, page, genre_name_request)
    await call.answer()


@search_by_genre_router.callback_query(F.data.startswith("get_genre"))
async def get_genre(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    id_genre = int(call.data.split(":")[-1])

    response = await api.genres.get_genre_by_id(id_genre)
    status = response.status

    if status != 200:
        await call.message.answer(
            l10n.format_value("search-by-genre-error-genre-unavailable")
        )
        await call.answer()
        return

    genre = response.get_model()

    response = await api.books.get_books_by_genre_id(id_genre)
    result = response.get_model()
    count = result.count
    books = result.books

    text = l10n.format_value(
        "search-by-genre-all-books",
        {"genre_name": genre.genre_name},
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
        reply_markup=genre_book_pagination_keyboard(
            l10n=l10n,
            found=count,
            books=books,
            id_genre=id_genre,
        ),
    )
    await state.clear()
    await call.answer()


@search_by_genre_router.callback_query(F.data.startswith("genre_book_page"))
async def genre_book_page(call: CallbackQuery, l10n: FluentLocalization):
    page = int(call.data.split(":")[-2])
    id_genre = int(call.data.split(":")[-1])

    response = await api.books.get_books_by_genre_id(id_genre, page=page)
    result = response.get_model()
    found = result.count
    books = result.books

    genre_name_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    text = l10n.format_value(
        "search-by-genre-all-books",
        {"genre_name": genre_name_request},
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

    await call.message.edit_text(
        text=text,
        reply_markup=genre_book_pagination_keyboard(
            l10n=l10n,
            found=found,
            books=books,
            id_genre=id_genre,
            page=page,
        ),
    )
    await call.answer()


async def genre_search(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    page: int = 1,
    genre_name_request: str = None,
):
    """
    A common function for handling genre searches and forward/backward button presses.
    :param message: Message or callback object.
    :param l10n: Language set by the user.
    :param state: Search state.
    :param page: Page number for pagination.
    :param genre_name_request: Name of the genre to search for.
    """

    if genre_name_request is None:
        genre_name_request = message.text

    genre_name_request = genre_name_request.replace('"', "")

    if len(genre_name_request) > 255:
        await message.answer(
            l10n.format_value("search-by-genre-error-genre-name-too-long"),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.GENRE),
        )
        return

    response = await api.genres.search_genres(genre_name_request, page=page)
    result = response.get_model()
    found = result.found
    genres = result.genres

    if found == 0:
        await message.answer(
            l10n.format_value(
                "search-by-genre-error-not-found",
                {"genre_name_request": genre_name_request},
            ),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.AUTHOR),
        )
        return

    if found == 1:
        genre = genres[0].genre
        id_genre = genre.id_genre

        response = await api.books.get_books_by_genre_id(id_genre)
        result = response.get_model()
        count = result.count
        books = result.books

        text = l10n.format_value(
            "search-by-genre-all-books",
            {"genre_name": genre.genre_name},
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
                text=text,
                reply_markup=genre_book_pagination_keyboard(
                    l10n=l10n,
                    found=count,
                    books=books,
                    id_genre=id_genre,
                    page=page,
                ),
            )
        except TelegramBadRequest:
            await message.answer(
                text=text,
                reply_markup=genre_book_pagination_keyboard(
                    l10n=l10n,
                    found=count,
                    books=books,
                    id_genre=id_genre,
                    page=page,
                ),
            )
        await state.clear()
        return

    text = l10n.format_value(
        "search-by-genre-success",
        {"genre_name_request": genre_name_request},
    )
    genre_number = ((page - 1) * 5) + 1

    for genre in genres:
        genre = genre.genre
        genre_name = genre.genre_name
        text += f"\n\n<b>{genre_number}.</b> <code>{genre_name}</code>"
        genre_number += 1
    try:
        await message.edit_text(
            text=text,
            reply_markup=genre_pagination_keyboard(
                l10n=l10n,
                genres=genres,
                found=found,
                page=page,
            ),
        )
    except TelegramBadRequest:
        await message.answer(
            text=text,
            reply_markup=genre_pagination_keyboard(
                l10n=l10n,
                genres=genres,
                found=found,
                page=page,
            ),
        )
