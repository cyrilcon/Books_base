from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.config import config


def discount_50_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Discount 50%" button is formed.
    :param l10n: Language set by the user.
    :return: The "Discount 50%" button.
    """

    discount_50 = InlineKeyboardButton(
        text=l10n.format_value("button-discount-50"),
        callback_data=f"discount:50:{config.price.discount.discount_50}",
    )
    return discount_50
