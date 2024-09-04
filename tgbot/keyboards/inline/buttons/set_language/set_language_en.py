from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def set_language_en_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "ENG" button is formed.
    :param l10n: Language set by the user.
    :return: The "ENG" button.
    """

    set_language_en = InlineKeyboardButton(
        text=l10n.format_value("button-language-en"),
        callback_data="set_language:en",
    )
    return set_language_en
