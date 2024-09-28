from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import buy_deep_link_button


def buy_deep_link_keyboard(deep_link_url: str) -> InlineKeyboardMarkup:
    """
    The "Buy" deep link keyboard is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "Buy" deep link keyboard.
    """

    buy_deep_link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                buy_deep_link_button(deep_link_url),
            ]
        ],
    )
    return buy_deep_link_markup
