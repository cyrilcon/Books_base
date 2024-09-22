from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def book_paid_button(
    l10n: FluentLocalization,
    price: int | float,
    id_payment: str,
) -> InlineKeyboardButton:
    """
    The "Paid" button is formed.
    :param l10n: Language set by the user.
    :param price: Product price.
    :param id_payment: Unique payment identifier.
    :return: The "Paid" button.
    """

    book_paid = InlineKeyboardButton(
        book_paid=l10n.format_value("button-paid"),
        callback_data=f"book_paid:{price}:{id_payment}",
    )
    return book_paid
