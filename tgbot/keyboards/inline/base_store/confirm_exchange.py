from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def confirm_exchange_keyboard(l10n, discount: int, price: int) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "« Назад" и "Обменять".
    :param l10n: Язык установленный у пользователя.
    :param discount: Скидка выбранная пользователем.
    :param price: Цена скидки в base.
    :return: Кнопки "« Назад" и "Обменять".
    """

    confirm_exchange_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=l10n.format_value("button-back"),
                    callback_data="back-to-exchange",
                ),
                InlineKeyboardButton(
                    text=l10n.format_value("button-exchange"),
                    callback_data=f"confirm-exchange:{discount}:{price}",
                ),
            ]
        ],
    )
    return confirm_exchange_buttons
