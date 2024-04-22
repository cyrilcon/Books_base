from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def done_clear_cancel_keyboard(l10n):
    """
    Формируются кнопки "Готово", "Стереть" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "Готово", "Стереть" и "Отмена".
    """

    done_clear_cancel_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-done"), callback_data="done"
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-clear"), callback_data="clear"
                ),
            ],
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                )
            ],
        ],
    )
    return done_clear_cancel_buttons
