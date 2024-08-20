from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    language_en_button,
    language_ru_button,
    language_uk_button,
)


def set_language_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "set_languages" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "languages" keyboard.
    """

    set_languages_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                language_en_button(l10n),
                language_ru_button(l10n),
                language_uk_button(l10n),
            ],
        ],
    )
    return set_languages_markup
