from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import read_button


def my_books_keyboard(
    l10n: FluentLocalization,
    book_ids: List[int],
    page: int = 1,
) -> InlineKeyboardMarkup:
    """
    A keyboard with pagination for my books.
    :param l10n: Language set by the user.
    :param book_ids: List of book ids.
    :param page: Page number for pagination.
    :return: Keyboard with pagination for my books.
    """

    action_buttons = []

    books_count = len(book_ids)

    if books_count > 1:
        if page > 1:
            action_buttons.append(
                InlineKeyboardButton(text=f"⬅️", callback_data=f"my_books_page:{page-1}")
            )

        action_buttons.append(
            InlineKeyboardButton(
                text=f"{l10n.format_value("page")} {page}/{books_count}",
                callback_data=f"pagination_info:{page}:{books_count}",
            )
        )

        if page < books_count:
            action_buttons.append(
                InlineKeyboardButton(text=f"➡️", callback_data=f"my_books_page:{page+1}")
            )

    my_books_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                read_button(l10n, id_book=book_ids[page - 1]),
            ],
            action_buttons,
        ]
    )

    return my_books_markup
