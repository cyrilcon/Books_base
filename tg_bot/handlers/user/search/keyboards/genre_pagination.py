from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    search_by_author_button,
    search_by_title_button,
)
from api.api_v1.schemas import GenreSearchResult


def genre_pagination_keyboard(
    l10n: FluentLocalization,
    genres: List[GenreSearchResult],
    found: int = None,
    page: int = 1,
) -> InlineKeyboardMarkup:
    """
    The pagination keyboard for genre search is formed.
    :param l10n: Language set by the user.
    :param genres: List of genres.
    :param found: Number of genres found by search.
    :param page: Page number for pagination.
    :return: The pagination keyboard.
    """

    numbers_buttons = []
    genre_number = ((page - 1) * 5) + 1

    for genre in genres:
        genre = genre.genre
        id_genre_button = InlineKeyboardButton(
            text=f"{genre_number}", callback_data=f"get_genre:{genre.id_genre}"
        )
        numbers_buttons.append(id_genre_button)
        genre_number += 1

    pagination_buttons = []

    if page > 1:
        pagination_buttons.append(
            InlineKeyboardButton(text=f"⬅️", callback_data=f"genre_page:{page-1}")
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
                InlineKeyboardButton(text=f"➡️", callback_data=f"genre_page:{page+1}")
            )

    genre_pagination_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            numbers_buttons,
            pagination_buttons,
            [
                search_by_author_button(l10n),
                search_by_title_button(l10n),
            ],
        ]
    )
    return genre_pagination_markup
