from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def files_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Files" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Files" button.
    """

    files = InlineKeyboardButton(
        text=l10n.format_value("button-files"),
        callback_data=f"edit_files:{id_book}",
    )
    return files
