from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import (
    price_update_85_button,
    price_update_50_button,
)


def price_update_keyboard(l10n, id_book: int) -> InlineKeyboardMarkup:
    """
    The "85₽" and "50₽" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book)
    :return: The "85₽" and "50₽" keyboard.
    """

    price_update_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                price_update_85_button(l10n, id_book=id_book),
                price_update_50_button(l10n, id_book=id_book),
            ],
        ],
    )
    return price_update_markup
