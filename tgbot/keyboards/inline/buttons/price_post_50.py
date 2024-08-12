from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def price_post_50_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "50₽" button is formed.
    :param l10n: Language set by the user.
    :return: The "50₽" button.
    """

    price_post_50 = InlineKeyboardButton(
        text=l10n.format_value("button-price-50"),
        callback_data="price_post_50",
    )
    return price_post_50
