from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import deep_link_set_button


def deep_link_set_keyboard(deep_link_url: str) -> InlineKeyboardMarkup:
    """
    The "Set" deep link keyboard is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "set" deep link keyboard.
    """

    deep_link_set_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                deep_link_set_button(deep_link_url),
            ]
        ],
    )
    return deep_link_set_markup
