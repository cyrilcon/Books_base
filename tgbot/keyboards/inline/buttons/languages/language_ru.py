from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def language_ru_button(l10n: FluentLocalization) -> InlineKeyboardButton:
    """
    The "RUS" button is formed.
    :param l10n: Language set by the user.
    :return: The "RUS" button.
    """

    language_ru = InlineKeyboardButton(
        text=l10n.format_value("button-ru"),
        callback_data="set_language:ru",
    )
    return language_ru
