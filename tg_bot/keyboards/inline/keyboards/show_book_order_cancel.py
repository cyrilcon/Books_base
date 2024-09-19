from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    show_book_button,
    order_button,
    cancel_button,
)


def show_book_order_cancel_keyboard(
    l10n: FluentLocalization, id_book: int
) -> InlineKeyboardMarkup:
    """
    The "show_book_order_cancel" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :return: The "show_book_order_cancel" keyboard.
    """

    show_booking_cancel_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                show_book_button(l10n, id_book=id_book),
            ],
            [
                order_button(l10n),
            ],
            [
                cancel_button(l10n),
            ],
        ],
    )
    return show_booking_cancel_markup
