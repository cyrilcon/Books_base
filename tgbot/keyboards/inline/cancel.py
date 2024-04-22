from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def cancel_keyboard(l10n):
    """
    Формируется кнопка "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопка "Отмена".
    """

    cancel_button = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                )
            ]
        ],
    )
    return cancel_button
