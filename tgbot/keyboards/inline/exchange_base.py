from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def exchange_base_keyboard(l10n) -> InlineKeyboardMarkup:
    """
    Формируется кнопка "Обменять".
    :param l10n: Язык установленный у пользователя.
    :return: Кнопка "Обменять".
    """

    exchange_base_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-exchange"), callback_data="exchange"
                )
            ]
        ],
    )
    return exchange_base_button
