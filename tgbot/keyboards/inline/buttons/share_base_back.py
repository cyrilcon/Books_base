from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def share_base_back_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Back" button is formed.
    :param l10n: Language set by the user.
    :return: The "Back" button.
    """

    share_base_back = InlineKeyboardButton(
        text=l10n.format_value("button-back"),
        callback_data="share_base_back",
    )
    return share_base_back
