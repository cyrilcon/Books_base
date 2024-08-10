from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def price_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Price" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Price" button.
    """

    price = InlineKeyboardButton(
        text=l10n.format_value("button-price"),
        callback_data=f"price:{id_book}",
    )
    return price
