from aiogram.types import InlineKeyboardMarkup

from tg_bot.keyboards.inline.buttons import (
    price_85_button,
    price_50_button,
    cancel_button,
)


def edit_price_keyboard(l10n, id_book: int) -> InlineKeyboardMarkup:
    """
    The "edit_price" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book)
    :return: The "edit_price" keyboard.
    """

    edit_price_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                price_85_button(l10n, id_book=id_book),
                price_50_button(l10n, id_book=id_book),
            ],
            [
                cancel_button(l10n),
            ],
        ],
    )
    return edit_price_markup
