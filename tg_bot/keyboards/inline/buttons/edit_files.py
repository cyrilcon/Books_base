from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_files_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit files" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit files" button.
    """

    edit_files = InlineKeyboardButton(
        text=l10n.format_value("button-files"),
        callback_data=f"edit_files:{id_book}",
    )
    return edit_files
