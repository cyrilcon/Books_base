from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def yes_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Yes" button is formed.
    :param l10n: Language set by the user.
    :return: The "Yes" button.
    """

    yes = InlineKeyboardButton(
        text=l10n.format_value("button-yes"),
        callback_data="yes",
    )
    return yes
