from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def unavailable_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Unavailable" button is formed.
    :param l10n: Language set by the user.
    :return: The "Unavailable" button.
    """

    unavailable = InlineKeyboardButton(
        text=l10n.format_value("button-unavailable"),
        callback_data="unavailable",
    )
    return unavailable
