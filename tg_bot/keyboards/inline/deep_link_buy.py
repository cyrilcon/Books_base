from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import deep_link_buy_button


def deep_link_buy_keyboard(deep_link_url: str) -> InlineKeyboardMarkup:
    """
    The "Buy" deep link keyboard is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "Buy" deep link keyboard.
    """

    deep_link_buy_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                deep_link_buy_button(deep_link_url),
            ]
        ],
    )
    return deep_link_buy_markup
