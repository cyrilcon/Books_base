from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def create_price_50_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "50₽" button is formed.
    :param l10n: Language set by the user.
    :return: The "50₽" button.
    """

    create_price_50 = InlineKeyboardButton(
        text=l10n.format_value("button-price-50"),
        callback_data="create_price:50",
    )
    return create_price_50
