from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def back_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Back" button is formed.
    :param l10n: Language set by the user.
    :return: The "Back" button.
    """

    back = InlineKeyboardButton(
        text=l10n.format_value("button-back"),
        callback_data="back",
    )

    return back
