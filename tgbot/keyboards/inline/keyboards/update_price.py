from aiogram.types import InlineKeyboardMarkup

from tgbot.keyboards.inline.buttons import (
    update_price_85_button,
    update_price_50_button,
)


def update_price_keyboard(l10n, id_book: int) -> InlineKeyboardMarkup:
    """
    The "update_price" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book)
    :return: The "update_price" keyboard.
    """

    update_price_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                update_price_85_button(l10n, id_book=id_book),
                update_price_50_button(l10n, id_book=id_book),
            ],
        ],
    )
    return update_price_markup
