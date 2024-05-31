from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def booking_again_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируется кнопка "Заказать ещё".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопка "Заказать ещё".
    """

    cancel_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-booking-again"),
                    callback_data="booking_again",
                )
            ]
        ],
    )
    return cancel_button
