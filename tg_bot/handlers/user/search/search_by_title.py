import re

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionMiddleware
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from api.api_v1.schemas import UserSchema
from tg_bot.enums import SearchBy
from tg_bot.keyboards.inline import buy_or_read_keyboard
from tg_bot.services.data import BookFormatter, generate_book_caption
from tg_bot.services.utils import is_valid_book_article
from .keyboards import search_by_keyboard, book_pagination_keyboard

search_by_title_router = Router()
search_by_title_router.message.middleware(ChatActionMiddleware())


@search_by_title_router.callback_query(
    F.data.startswith("search_by_title"),
    flags={"safe_message": False},
)
async def search_by_title(
    call: CallbackQuery,
    l10n: FluentLocalization,
):
    await call.message.edit_text(
        l10n.format_value("search-by-title"),
        reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
    )
    await call.answer()


@search_by_title_router.message(
    F.text,
    flags={
        "chat_action": "typing",
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def search_by_title_process(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
):
    await book_search(message, l10n, user)


@search_by_title_router.callback_query(
    F.data.startswith("book_page"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def book_page(
    call: CallbackQuery,
    l10n: FluentLocalization,
    user: UserSchema,
):
    page = int(call.data.split(":")[-1])
    book_title_request = re.search(r'"([^"]*)"', call.message.text).group(1)

    await book_search(call.message, l10n, user, page, book_title_request)
    await call.answer()


@search_by_title_router.callback_query(
    F.data.startswith("get_book"),
    flags={"safe_message": False},
)
async def get_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
):
    await state.clear()

    id_book = int(call.data.split(":")[-1])
    article = BookFormatter.format_article(id_book)

    response = await api.books.get_book_by_id(id_book=id_book)

    if response.status != 200:
        await call.answer(
            l10n.format_value(
                "error-book-unavailable",
                {"article": article},
            ),
            show_alert=True,
        )
        return

    book = response.get_model()

    caption = await generate_book_caption(
        book_data=book,
        l10n=l10n,
        user=user,
    )

    await call.message.answer_photo(
        photo=book.cover,
        caption=caption,
        reply_markup=await buy_or_read_keyboard(
            l10n=l10n,
            id_book=id_book,
            user=user,
        ),
    )
    await call.answer()


async def book_search(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
    page: int = 1,
    book_title_request: str = None,
):
    """
    A common function for handling book searches and forward/backward button presses.
    :param message: Message or callback object.
    :param l10n: Language set by the user.
    :param user: User instance.
    :param page: Page number for pagination.
    :param book_title_request: Title of the book to search for.
    """

    if book_title_request is None:
        book_title_request = message.text

    if is_valid_book_article(book_title_request):
        id_book = int(book_title_request.lstrip("#"))
        response = await api.books.get_book_by_id(id_book=id_book)

        if response.status != 200:
            await message.answer(
                l10n.format_value(
                    "search-by-title-error-article-not-found",
                    {"article": book_title_request},
                ),
                reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
            )
            return

        book = response.get_model()

        caption = await generate_book_caption(
            book_data=book,
            l10n=l10n,
            user=user,
        )

        await message.answer_photo(
            photo=book.cover,
            caption=caption,
            reply_markup=await buy_or_read_keyboard(
                l10n=l10n,
                id_book=book.id_book,
                user=user,
            ),
        )
        return

    book_title_request = book_title_request.replace('"', "")

    if len(book_title_request) > 255:
        await message.answer(
            l10n.format_value("search-by-title-error-title-too-long"),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
        )
        return

    response = await api.books.search_books_by_title(
        title=book_title_request,
        page=page,
    )
    result = response.get_model()
    found = result.found
    books = result.books

    if found == 0:
        await message.answer(
            l10n.format_value(
                "search-by-title-error-title-not-found",
                {"book_title_request": book_title_request},
            ),
            reply_markup=search_by_keyboard(l10n, by=SearchBy.TITLE),
        )
        return

    if found == 1:
        book = books[0].book
        caption = await generate_book_caption(
            book_data=book,
            l10n=l10n,
            user=user,
        )
        await message.answer_photo(
            photo=book.cover,
            caption=caption,
            reply_markup=await buy_or_read_keyboard(
                l10n=l10n,
                id_book=book.id_book,
                user=user,
            ),
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

    keyboard = book_pagination_keyboard(
        l10n=l10n,
        found=found,
        books=books,
        page=page,
    )
    try:
        await message.edit_text(text=text, reply_markup=keyboard)
    except TelegramBadRequest:
        await message.answer(text=text, reply_markup=keyboard)
