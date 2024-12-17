from aiogram.types import InlineKeyboardButton


def link_buy_button(url: str) -> InlineKeyboardButton:
    """
    The "Buy" deep link button is formed.
    :param url: Link to purchase the book.
    :return: The "Buy" deep link button.
    """

    link_buy = InlineKeyboardButton(
        text="Купить",
        callback_data=f"link_buy",
        url=url,
    )
    return link_buy
