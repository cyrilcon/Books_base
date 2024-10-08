from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.config import config


def discount_15_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Discount 15%" button is formed.
    :param l10n: Language set by the user.
    :return: The "Discount 15%" button.
    """

    discount_15 = InlineKeyboardButton(
        text=l10n.format_value("button-discount-15"),
        callback_data=f"discount:15:{config.price.discount.discount_15}",
    )
    return discount_15
