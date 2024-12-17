from aiogram.types import InlineKeyboardButton


def link_set_button(url: str) -> InlineKeyboardButton:
    """
    The "Set" deep link button is formed.
    :param url: Link to purchase the book.
    :return: The "Set" deep link button.
    """

    link_set = InlineKeyboardButton(
        text="📚 Собрать набор",
        callback_data=f"link_set",
        url=url,
    )
    return link_set
