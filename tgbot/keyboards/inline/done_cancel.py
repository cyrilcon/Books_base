from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def done_cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "Готово" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "Готово" и "Отмена".
    """

    done_cancel_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-done"), callback_data="done"
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                ),
            ]
        ],
    )
    return done_cancel_buttons
