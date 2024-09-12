from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    search_by_title_button,
    search_by_genre_button,
)
from tgbot.schemas import AuthorSearchResult


def author_search_pagination_keyboard(
    l10n: FluentLocalization,
    found: int,
    authors: List[AuthorSearchResult],
    page: int = 1,
) -> InlineKeyboardMarkup:
    """
    The pagination keyboard for author search is formed.
    :param l10n: Language set by the user.
    :param found: Number of authors found by search.
    :param authors: List of authors.
    :param page: Page number for pagination.
    :return: The pagination keyboard.
    """

    numbers_buttons = []
    author_number = ((page - 1) * 5) + 1

    for author in authors:
        author = author.author
        id_author_button = InlineKeyboardButton(
            text=f"{author_number}", callback_data=f"get_author:{author.id_author}"
        )
        numbers_buttons.append(id_author_button)
        author_number += 1

    pagination_buttons = []

    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(
                text=f"⬅️", callback_data=f"author_search_page:{page-1}"
            )
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
                InlineKeyboardButton(
                    text=f"➡️", callback_data=f"author_search_page:{page+1}"
                )
            )

    author_search_pagination_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            numbers_buttons,
            pagination_buttons,
            [
                search_by_title_button(l10n),
                search_by_genre_button(l10n),
            ],
        ]
    )
    return author_search_pagination_markup
