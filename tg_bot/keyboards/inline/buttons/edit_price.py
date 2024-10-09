from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_price_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit price" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit price" button.
    """

    edit_price = InlineKeyboardButton(
        text=l10n.format_value("button-edit-price"),
        callback_data=f"edit_price:{id_book}",
    )
    return edit_price
