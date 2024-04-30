from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def edit_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки для редактирования книги.
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки для редактирования книги.
    """

    edit_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-article"),
                    callback_data="edit_article",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-title"),
                    callback_data="edit_title",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-authors"),
                    callback_data="edit_authors",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-descriptions"),
                    callback_data="edit_descriptions",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-genres"),
                    callback_data="edit_genres",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-cover"),
                    callback_data="edit_cover",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-files"),
                    callback_data="edit_files",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-edit-book-price"),
                    callback_data="edit_price",
                ),
            ],
        ],
    )
    return edit_buttons
