from aiogram.types import InlineKeyboardButton


def buy_book_deep_link_button(deep_link_url: str) -> InlineKeyboardButton:
    """
    The "Buy book" deep link button is formed.
    :param deep_link_url: Link to purchase the book.
    :return: The "Buy book" deep link button.
    """

    buy_book_deep_link = InlineKeyboardButton(
        text="Купить",
        callback_data=f"buy_book_deep_link",
        url=f"{deep_link_url}",
    )
    return buy_book_deep_link
