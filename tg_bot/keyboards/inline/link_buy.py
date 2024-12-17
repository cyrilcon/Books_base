from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import link_buy_button


def link_buy_keyboard(link: str) -> InlineKeyboardMarkup:
    """
    The "Buy" deep link keyboard is formed.
    :param link: Link to purchase the book.
    :return: The "Buy" deep link keyboard.
    """

    link_buy_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                link_buy_button(link),
            ]
        ],
    )
    return link_buy_markup
