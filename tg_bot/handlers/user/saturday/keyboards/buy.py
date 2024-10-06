from typing import List

from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import buy_set_button


def buy_keyboard(
    l10n: FluentLocalization,
    book_ids: List[int],
) -> InlineKeyboardMarkup:
    """
    The "buy" keyboard is formed.
    :param l10n: Language set by the user.
    :param book_ids: List of book ids.
    :return: The "buy" keyboard.
    """

    buy_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                buy_set_button(l10n, book_ids=book_ids),
            ],
        ],
    )
    return buy_markup
