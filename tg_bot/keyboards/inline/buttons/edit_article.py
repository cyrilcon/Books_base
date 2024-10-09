from aiogram.types import InlineKeyboardButton
from fluent.runtime import FluentLocalization


def edit_article_button(l10n: FluentLocalization, id_book: int) -> InlineKeyboardButton:
    """
    The "Edit article" button is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "Edit article" button.
    """

    edit_article = InlineKeyboardButton(
        text=l10n.format_value("button-edit-article"),
        callback_data=f"edit_article:{id_book}",
    )
    return edit_article
