from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    language_ru_button,
    language_en_button,
    language_uk_button,
)


def languages_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "languages" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "languages" keyboard.
    """

    languages_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                language_ru_button(l10n),
                language_en_button(l10n),
                language_uk_button(l10n),
            ],
        ],
    )
    return languages_markup
