from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import buy_book_deep_link_button


def buy_book_deep_link_keyboard(deep_link_url: str) -> InlineKeyboardMarkup:
    """
    The "Buy book" deep link keyboard is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "Buy" deep link keyboard.
    """

    buy_book_deep_link_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                buy_book_deep_link_button(deep_link_url),
            ]
        ],
    )
    return buy_book_deep_link_markup
