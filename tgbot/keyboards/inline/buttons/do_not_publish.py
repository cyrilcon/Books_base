from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def do_not_publish_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "Don't publish" button is formed.
    :param l10n: Language set by the user.
    :return: The "Don't publish" button.
    """

    do_not_publish = InlineKeyboardButton(
        text=l10n.format_value("button-do-not-publish"),
        callback_data="do_not_publish",
    )
    return do_not_publish
