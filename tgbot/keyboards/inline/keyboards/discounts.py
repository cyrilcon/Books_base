from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import (
    discount_15_button,
    discount_30_button,
    discount_50_button,
    discount_100_button,
)


def discounts_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "discounts" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "discounts" keyboard.
    """

    discounts_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                discount_15_button(l10n),
                discount_30_button(l10n),
                discount_50_button(l10n),
            ],
            [
                discount_100_button(l10n),
            ],
        ],
    )
    return discounts_markup
