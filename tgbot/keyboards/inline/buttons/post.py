from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def post_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Post" button is formed.
    :param l10n: Language set by the user.
    :return: The "Post" button.
    """

    post = InlineKeyboardButton(
        text=l10n.format_value("button-post"),
        callback_data="post",
    )
    return post
