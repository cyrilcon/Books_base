from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def read_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Read" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Read" button.
    """

    read = InlineKeyboardButton(
        text=l10n.format_value("button-read"),
        callread_data=f"read:{id_book}",
    )
    return read
