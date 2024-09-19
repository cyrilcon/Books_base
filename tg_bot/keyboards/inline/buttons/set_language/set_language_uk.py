from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def set_language_uk_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "UKR" button is formed.
    :param l10n: Language set by the user.
    :return: The "UKR" button.
    """

    set_language_uk = InlineKeyboardButton(
        text=l10n.format_value("button-language-uk"),
        callback_data="set_language:uk",
    )
    return set_language_uk
