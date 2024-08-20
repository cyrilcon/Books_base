from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def language_uk_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "UKR" button is formed.
    :param l10n: Language set by the user.
    :return: The "UKR" button.
    """

    language_uk = InlineKeyboardButton(
        text=l10n.format_value("button-uk"),
        callback_data="set_language:uk",
    )
    return language_uk
