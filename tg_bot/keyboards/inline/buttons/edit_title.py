from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_title_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit title" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit title" button.
    """

    edit_title = InlineKeyboardButton(
        text=l10n.format_value("button-edit-title"),
        callback_data=f"edit_title:{id_book}",
    )
    return edit_title
