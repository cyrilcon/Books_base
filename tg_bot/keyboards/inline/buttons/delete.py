from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def delete_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Delete" button is formed.
    :param l10n: Language set by the user.
    :return: The "Delete" button.
    """

    delete = InlineKeyboardButton(
        text=l10n.format_value("button-delete"),
        callback_data="delete",
    )
    return delete
