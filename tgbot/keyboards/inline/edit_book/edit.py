from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_keyboard(l10n, id_book: int) -> InlineKeyboardMarkup:
    """
    Формируются кнопки для редактирования книги.
    :param l10n: Язык установленный у пользователя.
    :param id_book: Артикул книги, данные которой будут изменяться.
    :return: Кнопки для редактирования книги.
    """

    edit_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-article"),
                    callback_data=f"edit_article:{id_book}",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-title"),
                    callback_data=f"edit_title:{id_book}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-authors"),
                    callback_data=f"edit_authors:{id_book}",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-descriptions"),
                    callback_data=f"edit_descriptions:{id_book}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-genres"),
                    callback_data=f"edit_genres:{id_book}",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-cover"),
                    callback_data=f"edit_cover:{id_book}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-files"),
                    callback_data=f"edit_files:{id_book}",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-price"),
                    callback_data=f"edit_price:{id_book}",
                ),
            ],
        ],
    )
    return edit_buttons
