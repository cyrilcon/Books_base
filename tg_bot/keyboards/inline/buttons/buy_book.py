from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def buy_book_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Buy book" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Buy book" button.
    """

    buy_book = InlineKeyboardButton(
        text=l10n.format_value("button-buy"),
        callback_data=f"buy_book:{id_book}",
    )
    return buy_book
