from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def order_again_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Order again" button is formed.
    :param l10n: Language set by the user.
    :return: The "Order again" button.
    """

    order_again = InlineKeyboardButton(
        text=l10n.format_value("button-order-again"),
        callback_data="order_again",
    )
    return order_again
