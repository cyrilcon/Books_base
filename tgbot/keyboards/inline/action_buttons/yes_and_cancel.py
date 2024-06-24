from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_and_cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "Да" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "Да" и "Отмена".
    """

    yes_and_cancel_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-yes"), callback_data="yes"
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                ),
            ]
        ],
    )
    return yes_and_cancel_buttons
