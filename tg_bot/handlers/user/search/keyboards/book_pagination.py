from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    search_by_author_button,
    search_by_genre_button,
)
from api.books_base_api.schemas import BookTitleSimilarityResult


def book_pagination_keyboard(
    l10n: FluentLocalization,
    found: int,
    books: List[BookTitleSimilarityResult],
    page: int = 1,
) -> InlineKeyboardMarkup:
    """
    The pagination keyboard for book search is formed.
    :param l10n: Language set by the user.
    :param found: Number of books found by search.
    :param books: List of books.
    :param page: Page number for pagination.
    :return: The pagination keyboard.
    """

    numbers_buttons = []
    book_number = ((page - 1) * 5) + 1

    for book in books:
        book = book.book
        id_book_button = InlineKeyboardButton(
            text=f"{book_number}", callback_data=f"get_book:{book.id_book}"
        )
        numbers_buttons.append(id_book_button)
        book_number += 1

    pagination_buttons = []

    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text=f"⬅️", callback_data=f"book_page:{page-1}")
        )
    if found > 5:
        all_pages = (found + 4) // 5
        pagination_buttons.append(
            InlineKeyboardButton(
                text=f"{l10n.format_value("page")} {page}/{all_pages}",
                callback_data=f"pagination_info:{page}:{all_pages}",
            )
        )

        if min(page * 5, found) < found:
            pagination_buttons.append(
                InlineKeyboardButton(text=f"➡️", callback_data=f"book_page:{page+1}")
            )

    book_pagination_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            numbers_buttons,
            pagination_buttons,
            [
                search_by_author_button(l10n),
                search_by_genre_button(l10n),
            ],
        ]
    )
    return book_pagination_markup
