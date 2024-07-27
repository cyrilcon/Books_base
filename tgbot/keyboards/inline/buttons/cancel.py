from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def cancel_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Cancel" button is formed.
    :param l10n: Language set by the user.
    :return: The "Cancel" button.
    """

    cancel = InlineKeyboardButton(
        text=l10n.format_value("button-cancel"),
        callback_data="cancel",
    )

    return cancel
