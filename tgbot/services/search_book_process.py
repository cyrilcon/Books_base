from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import (
    search_by_author_and_genre_keyboard,
    pagination_keyboard,
)
from tgbot.services import generate_book_caption, BookFormatter


async def search_book_process(
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

    book_title_request.replace('"', "")

    if len(book_title_request) > 255:
        await message.answer(
            l10n.format_value("search-by-title-error-title-too-long"),
            reply_markup=search_by_author_and_genre_keyboard(l10n),
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
            reply_markup=search_by_author_and_genre_keyboard(l10n),
        )
        return

    if found == 1:
        book = books[0]
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
    num = ((page - 1) * 5) + 1

    for book in books:
        book = book.book

        article = BookFormatter.format_article(book.id_book)
        title = book.title
        authors = book.authors
        text += (
            f"\n\n<b>{num}.</b> <code>{title}</code>\n"
            f"{', '.join(f'<code>{author.author_name.title()}</code>' for author in authors)}"
            f" (<code>{article}</code>)"
        )
        num += 1
    try:
        await message.edit_text(
            text, reply_markup=pagination_keyboard(l10n, found, books, page)
        )
    except TelegramBadRequest:
        await message.answer(
            text, reply_markup=pagination_keyboard(l10n, found, books, page)
        )
