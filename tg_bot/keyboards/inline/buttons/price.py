from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def price_button(
    l10n: FluentLocalization,
    price: int,
    id_book: int | None = None,
) -> InlineKeyboardButton:
    """
    The "Price" button is formed.
    :param l10n: Language set by the user.
    :param price: Product price.
    :param id_book: Unique book identifier (article of the book)
    :return: The "Price" button.
    """

    price = InlineKeyboardButton(
        text=l10n.format_value(f"button-price-{price}"),
        callback_data=f"price:{price}" + f":{id_book}" if id_book else f"price:{price}",
    )
    return price
