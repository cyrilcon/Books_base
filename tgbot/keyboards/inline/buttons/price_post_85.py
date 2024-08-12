from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def price_price_85_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "85₽" button is formed.
    :param l10n: Language set by the user.
    :return: The "85₽" button.
    """

    price_post_85 = InlineKeyboardButton(
        text=l10n.format_value("button-price-85"),
        callback_data="price_post_85",
    )
    return price_post_85
