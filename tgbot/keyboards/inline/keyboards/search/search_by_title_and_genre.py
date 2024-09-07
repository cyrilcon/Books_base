from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    search_by_title_button,
    search_by_genre_button,
)


def search_by_title_and_genre_keyboard(
    l10n: FluentLocalization,
) -> InlineKeyboardMarkup:
    """
    The "search_by_title_and_genre" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "search_by_title_and_genre" keyboard.
    """

    search_by_title_and_genre_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                search_by_title_button(l10n),
                search_by_genre_button(l10n),
            ],
        ],
    )
    return search_by_title_and_genre_markup
