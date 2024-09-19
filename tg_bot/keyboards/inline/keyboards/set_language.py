from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    set_language_en_button,
    set_language_ru_button,
    set_language_uk_button,
)


def set_language_keyboard(l10n: FluentLocalization) -> InlineKeyboardMarkup:
    """
    The "set_language" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "set_language" keyboard.
    """

    set_language_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                set_language_en_button(l10n),
                set_language_ru_button(l10n),
                set_language_uk_button(l10n),
            ],
        ],
    )
    return set_language_markup
