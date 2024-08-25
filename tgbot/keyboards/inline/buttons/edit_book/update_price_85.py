from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def update_price_85_button(
    l10n: FluentLocalization, id_book: int
) -> InlineKeyboardButton:
    """
    The "85₽" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book)
    :return: The "85₽" button.
    """

    update_price_85 = InlineKeyboardButton(
        text=l10n.format_value("button-price-85"),
        callback_data=f"update_price:85:{id_book}",
    )
    return update_price_85
