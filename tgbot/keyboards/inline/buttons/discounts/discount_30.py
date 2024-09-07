from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def discount_30_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Discount 30%" button is formed.
    :param l10n: Language set by the user.
    :return: The "Discount 30%" button.
    """

    discount_30 = InlineKeyboardButton(
        text=l10n.format_value("button-discount-30"),
        callback_data="discount:30:35",
    )
    return discount_30
