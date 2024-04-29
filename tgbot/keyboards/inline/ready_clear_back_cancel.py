from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ready_clear_back_cancel_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "Готово", "Стереть", "« Назад" и "Отмена".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "Готово", "Стереть", "« Назад" и "Отмена".
    """

    ready_clear_back_cancel_buttons = InlineKeyboardMarkup(
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
                    text=l10n.format_value("button-back"), callback_data="back"
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-cancel"), callback_data="cancel"
                ),
            ],
        ],
    )
    return ready_clear_back_cancel_buttons
