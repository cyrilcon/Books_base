from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def show_book_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Show book" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Show book" button.
    """

    show_book = InlineKeyboardButton(
        text=l10n.format_value("button-show-book"),
        callback_data=f"show_book:{id_book}",
    )
    return show_book
