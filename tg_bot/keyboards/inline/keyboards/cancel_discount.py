from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import cancel_discount_button


def cancel_discount_keyboard(
    l10n: FluentLocalization, discount: int
) -> InlineKeyboardMarkup:
    """
    The "cancel_discount" keyboard is formed.
    :param l10n: Language set by the user.
    :param discount: Discount value.
    :return: The "cancel_discount" keyboard.
    """

    cancel_discount_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                cancel_discount_button(l10n, discount=discount),
            ]
        ],
    )
    return cancel_discount_markup
