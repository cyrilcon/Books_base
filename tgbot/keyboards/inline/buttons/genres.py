from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def genres_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Genres" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Genres" button.
    """

    genres = InlineKeyboardButton(
        text=l10n.format_value("button-genres"),
        callback_data=f"genres:{id_book}",
    )
    return genres
