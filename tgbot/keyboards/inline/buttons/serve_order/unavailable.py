from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def unavailable_button(l10n: FluentLocalization, id_order: int) -> InlineKeyboardButton:
    """
    The "Unavailable" button is formed.
    :param l10n: Language set by the user.
    :param id_order: Unique order identifier.
    :return: The "Unavailable" button.
    """

    unavailable = InlineKeyboardButton(
        text=l10n.format_value("button-unavailable"),
        callback_data=f"book_unavailable:{id_order}",
    )
    return unavailable
