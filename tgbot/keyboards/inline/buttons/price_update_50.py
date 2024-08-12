from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def price_update_50_button(
    l10n: FluentLocalization, id_book: int
) -> InlineKeyboardButton:
    """
    The "50₽" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book)
    :return: The "50₽" button.
    """

    price_update_50 = InlineKeyboardButton(
        text=l10n.format_value("button-price-50"),
        callback_data=f"update_price:50:{id_book}",
    )
    return price_update_50
