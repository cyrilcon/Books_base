from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def search_by_author_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Search by author" button is formed.
    :param l10n: Language set by the user.
    :return: The "Search by author" button.
    """

    search_by_author = InlineKeyboardButton(
        text=l10n.format_value("button-search-by-author"),
        callback_data="search_by_author",
    )
    return search_by_author
