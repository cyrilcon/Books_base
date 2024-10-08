from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.config import config


def discount_100_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Discount 100%" button is formed.
    :param l10n: Language set by the user.
    :return: The "Discount 100%" button.
    """

    discount_100 = InlineKeyboardButton(
        text=l10n.format_value("button-discount-100"),
        callback_data=f"discount:100:{config.price.discount.discount_100}",
    )
    return discount_100
