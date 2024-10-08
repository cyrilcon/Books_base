from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import (
    discount_15_button,
    discount_30_button,
    discount_50_button,
    discount_100_button,
    back_button,
    cancel_button,
)


def discounts_back_cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "discounts_back_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "discounts_back_cancel" keyboard.
    """

    discounts_back_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                discount_15_button(l10n),
                discount_30_button(l10n),
                discount_50_button(l10n),
            ],
            [
                discount_100_button(l10n),
            ],
            [
                back_button(l10n),
                cancel_button(l10n),
            ],
        ],
    )
    return discounts_back_cancel_markup
