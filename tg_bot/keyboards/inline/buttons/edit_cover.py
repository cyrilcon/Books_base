from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_cover_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit cover" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit cover" button.
    """

    edit_cover = InlineKeyboardButton(
        text=l10n.format_value("button-edit-cover"),
        callback_data=f"edit_cover:{id_book}",
    )
    return edit_cover
