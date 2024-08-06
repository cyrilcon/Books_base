from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def not_from_user_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Not from user" button is formed.
    :param l10n: Language set by the user.
    :return: The "Not from user" button.
    """

    not_from_user = InlineKeyboardButton(
        text=l10n.format_value("button-not-from-user"),
        callback_data="not_from_user",
    )
    return not_from_user
