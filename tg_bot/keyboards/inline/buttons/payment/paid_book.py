from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def paid_book_button(
    l10n: FluentLocalization,
    id_book: int,
    price: int | float,
    id_payment: str,
) -> InlineKeyboardButton:
    """
    The "Paid" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :param price: Product price.
    :param id_payment: Unique payment identifier.
    :return: The "Paid" button.
    """

    paid_book = InlineKeyboardButton(
        text=l10n.format_value("button-paid"),
        callback_data=f"paid:book:{id_book}:{price}:{id_payment}",
    )
    return paid_book
