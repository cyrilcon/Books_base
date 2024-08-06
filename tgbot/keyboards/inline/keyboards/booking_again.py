from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import booking_again_button


def booking_again_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "Booking again" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "Booking again" keyboard.
    """

    booking_again_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                booking_again_button(l10n),
            ]
        ],
    )
    return booking_again_markup
