from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_genres_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit genres" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit genres" button.
    """

    edit_genres = InlineKeyboardButton(
        text=l10n.format_value("button-genres"),
        callback_data=f"edit_genres:{id_book}",
    )
    return edit_genres
