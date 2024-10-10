from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import order_again_button


def order_again_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "order_again" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "order_again" keyboard.
    """

    order_again_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                order_again_button(l10n),
            ]
        ],
    )
    return order_again_markup
