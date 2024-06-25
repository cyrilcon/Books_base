from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def prices_keyboard(id_book: int) -> InlineKeyboardMarkup:
    """
    Формируются кнопки "85₽" и "50₽".
    :param id_book: ID книги
    :return: Кнопки "85₽" и "50₽".
    """

    prices_buttons = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="85₽", callback_data=f"update_price:85:{id_book}"
                ),
                InlineKeyboardButton(
                    text="50₽", callback_data=f"update_price:50:{id_book}"
                ),
            ]
        ],
    )
    return prices_buttons
