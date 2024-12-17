from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import link_set_button


def link_set_keyboard(link: str) -> InlineKeyboardMarkup:
    """
    The "Set" deep link keyboard is formed.
    :param link: Link to purchase the book.
    :return: The "set" deep link keyboard.
    """

    link_set_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                link_set_button(link),
            ]
        ],
    )
    return link_set_markup
