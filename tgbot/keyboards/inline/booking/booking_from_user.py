from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def booking_from_user_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "Обслужить" и "Нет в наличии".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопки "Обслужить" и "Нет в наличии".
    """

    booking_from_user_buttons = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-service"), callback_data="service"
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-not-available"),
                    callback_data="not-available",
                ),
            ]
        ],
    )
    return booking_from_user_buttons
