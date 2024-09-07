from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import (
    search_by_author_button,
    search_by_title_button,
)


def search_by_author_and_title_keyboard(
    l10n: FluentLocalization,
) -> InlineKeyboardMarkup:
    """
    The "search_by_author_and_title" keyboard is formed.
    :param l10n: Language set by the user.
    :return: The "search_by_author_and_title" keyboard.
    """

    search_by_author_and_title_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                search_by_author_button(l10n),
                search_by_title_button(l10n),
            ],
        ],
    )
    return search_by_author_and_title_markup
