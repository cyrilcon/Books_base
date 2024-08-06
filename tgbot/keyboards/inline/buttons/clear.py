from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def clear_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Clear" button is formed.
    :param l10n: Language set by the user.
    :return: The "Clear" button.
    """

    clear = InlineKeyboardButton(
        text=l10n.format_value("button-clear"),
        callback_data="clear",
    )
    return clear
