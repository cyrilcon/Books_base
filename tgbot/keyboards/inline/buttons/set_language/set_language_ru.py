from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def set_language_ru_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "RUS" button is formed.
    :param l10n: Language set by the user.
    :return: The "RUS" button.
    """

    set_language_ru = InlineKeyboardButton(
        text=l10n.format_value("button-language-ru"),
        callback_data="set_language:ru",
    )
    return set_language_ru
