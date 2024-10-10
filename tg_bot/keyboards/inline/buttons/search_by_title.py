from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def search_by_title_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Search by title" button is formed.
    :param l10n: Language set by the user.
    :return: The "Search by title" button.
    """

    search_by_title = InlineKeyboardButton(
        text=l10n.format_value("button-search-by-title"),
        callback_data="search_by_title",
    )
    return search_by_title
