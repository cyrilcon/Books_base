from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def book_unavailable_button(
    l10n: FluentLocalization, id_order: int
) -> InlineKeyboardButton:
    """
    The "Book unavailable" button is formed.
    :param l10n: Language set by the user.
    :param id_order: Unique order identifier.
    :return: The "Book unavailable" button.
    """

    book_unavailable = InlineKeyboardButton(
        text=l10n.format_value("button-unavailable"),
        callback_data=f"book_unavailable:{id_order}",
    )
    return book_unavailable
