from aiogram.types import InlineKeyboardButton


def deep_link_buy_button(deep_link_url: str) -> InlineKeyboardButton:
    """
    The "Buy" deep link button is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "Buy" deep link button.
    """

    deep_link_buy = InlineKeyboardButton(
        text="Купить",
        callback_data=f"deep_link_buy",
        url=f"{deep_link_url}",
    )

    return deep_link_buy
