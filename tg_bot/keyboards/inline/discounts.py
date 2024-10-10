from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import discount_button


def discounts_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    The "discounts" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "discounts" keyboard.
    """

    discounts_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                discount_button(l10n, discount_value=15),
                discount_button(l10n, discount_value=30),
                discount_button(l10n, discount_value=50),
            ],
            [
                discount_button(l10n, discount_value=100),
            ],
        ],
    )
    return discounts_markup
