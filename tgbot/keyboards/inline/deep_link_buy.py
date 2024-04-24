from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def deep_link_buy_keyboard(deep_link_url: str):
    """
    Формируется дип-линк кнопка "Купить".
    :param deep_link_url: Ссылка на покупку книги.
    :return: Кнопка "Купить".
    """

    deep_link_buy_button = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=f"deep_link_buy",
                    url=f"{deep_link_url}",
                )
            ],
        ],
    )
    return deep_link_buy_button
