from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.enums import SearchBy
from tg_bot.keyboards.inline.buttons import (
    search_by_author_button,
    search_by_title_button,
    search_by_genre_button,
)


def search_by_keyboard(l10n: FluentLocalization, by: SearchBy) -> InlineKeyboardMarkup:
    """
    The "search_by" keyboard is formed.
    :param l10n: Language set by the user.
    :param by: Search Criterion.
    :return: The "search_by" keyboard.
    """

    buttons = []

    if by != SearchBy.AUTHOR:
        buttons.append(search_by_author_button(l10n))
    if by != SearchBy.TITLE:
        buttons.append(search_by_title_button(l10n))
    if by != SearchBy.GENRE:
        buttons.append(search_by_genre_button(l10n))

    search_by_markup = InlineKeyboardMarkup(inline_keyboard=[buttons])

    return search_by_markup
