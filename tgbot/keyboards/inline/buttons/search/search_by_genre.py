from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def search_by_genre_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Search by genre" button is formed.
    :param l10n: Language set by the user.
    :return: The "Search by genre" button.
    """

    search_by_genre = InlineKeyboardButton(
        text=l10n.format_value("button-search-by-genre"),
        callback_data="search_by_genre",
    )
    return search_by_genre
