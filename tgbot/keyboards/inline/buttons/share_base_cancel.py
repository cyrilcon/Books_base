from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def share_base_cancel_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Cancel" button is formed.
    :param l10n: Language set by the user.
    :return: The "Cancel" button.
    """

    share_base_cancel = InlineKeyboardButton(
        text=l10n.format_value("button-cancel"),
        callback_data="share_base_cancel",
    )
    return share_base_cancel
