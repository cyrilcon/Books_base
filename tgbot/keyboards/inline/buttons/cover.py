from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def cover_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Cover" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Cover" button.
    """

    cover = InlineKeyboardButton(
        text=l10n.format_value("button-cover"),
        callback_data=f"cover:{id_book}",
    )
    return cover
