from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def booking_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Booking" button is formed.
    :param l10n: Language set by the user.
    :return: The "Booking" button.
    """

    booking = InlineKeyboardButton(
        text=l10n.format_value("button-booking"),
        callback_data="booking",
    )
    return booking
