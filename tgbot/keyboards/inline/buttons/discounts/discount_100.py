from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def discount_100_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Discount 100%" button is formed.
    :param l10n: Language set by the user.
    :return: The "Discount 100%" button.
    """

    discount_100 = InlineKeyboardButton(
        text=l10n.format_value("button-discount-100"),
        callback_data="discount:100:55",
    )
    return discount_100
