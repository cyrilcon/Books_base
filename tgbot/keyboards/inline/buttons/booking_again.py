from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def booking_again_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Booking again" button is formed.
    :param l10n: Language set by the user.
    :return: The "Booking again" button.
    """

    booking_again = InlineKeyboardButton(
        text=l10n.format_value("button-booking-again"),
        callback_data="booking_again",
    )
    return booking_again
