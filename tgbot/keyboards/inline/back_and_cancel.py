from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def back_and_cancel_keyboard(l10n):
    """
    Формируются кнопки "« Назад" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "« Назад" и "Отмена".
    """

    back_and_cancel_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-back"), callback_data="back"
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                ),
            ]
        ],
    )
    return back_and_cancel_buttons
