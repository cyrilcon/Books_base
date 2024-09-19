from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def order_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Order" button is formed.
    :param l10n: Language set by the user.
    :return: The "Order" button.
    """

    order = InlineKeyboardButton(
        text=l10n.format_value("button-order"),
        callback_data="order",
    )
    return order
