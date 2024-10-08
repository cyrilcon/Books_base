from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tg_bot.config import config


def discount_button(
    l10n: FluentLocalization,
    discount_value: int,
) -> InlineKeyboardButton:
    """
    The "Discount" button is formed.
    :param l10n: Language set by the user.
    :param discount_value: Discount value.
    :return: The "Discount" button.
    """

    discount_mapping = {
        15: config.price.discount.discount_15,
        30: config.price.discount.discount_30,
        50: config.price.discount.discount_50,
        100: config.price.discount.discount_100,
    }

    discount_price = discount_mapping.get(discount_value)

    discount = InlineKeyboardButton(
        text=l10n.format_value(f"button-discount", {"discount_value": discount_value}),
        callback_data=f"discount:{discount_value}:{discount_price}",
    )
    return discount
