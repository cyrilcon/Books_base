from aiogram.types import InlineKeyboardButton


def deep_link_set_button(deep_link_url: str) -> InlineKeyboardButton:
    """
    The "Set" deep link button is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "Set" deep link button.
    """

    deep_link_set = InlineKeyboardButton(
        text="📚 Собрать набор",
        callback_data=f"deep_link_buy",
        url=f"{deep_link_url}",
    )
    return deep_link_set
