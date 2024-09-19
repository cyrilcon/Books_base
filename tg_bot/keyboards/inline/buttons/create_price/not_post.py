from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def not_post_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Don't publish" button is formed.
    :param l10n: Language set by the user.
    :return: The "Don't publish" button.
    """

    not_post = InlineKeyboardButton(
        text=l10n.format_value("button-not-post"),
        callback_data="not_post:85",
    )
    return not_post
