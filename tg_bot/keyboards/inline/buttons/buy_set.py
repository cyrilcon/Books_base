from typing import List

from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def buy_set_button(
    l10n: FluentLocalization,
    book_ids: List[int],
) -> InlineKeyboardButton:
    """
    The "Buy set" button is formed.
    :param l10n: Language set by the user.
    :param book_ids: List of book ids.
    :return: The "Buy set" button.
    """

    buy_set = InlineKeyboardButton(
        text=l10n.format_value("button-buy"),
        callback_data=f"buy_set:{','.join(map(str, book_ids))}",
    )
    return buy_set
