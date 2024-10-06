from typing import List

from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def paid_set_button(
    l10n: FluentLocalization,
    book_ids: List[int],
    id_payment: str,
) -> InlineKeyboardButton:
    """
    The "Paid" button is formed.
    :param l10n: Language set by the user.
    :param book_ids: List of book ids.
    :param id_payment: Unique payment identifier.
    :return: The "Paid" button.
    """

    paid_set = InlineKeyboardButton(
        text=l10n.format_value("button-paid"),
        # callback_data=f"paid_set:{id_payment}:{','.join(map(str, book_ids))}",
        callback_data=f"paid_set:{id_payment}:9999,8888,7777",
    )
    return paid_set
