from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    pay_xtr_button,
    pay_rub_button,
    paid_book_button,
    cancel_payment_button,
)


def pay_book_keyboard(
    l10n: FluentLocalization,
    id_book: int,
    url_payment: str,
    price: int,
    id_payment: str,
):
    """
    The "pay_book" keyboard is formed.
    :param l10n: Language set by the user.
    :param id_book: Unique book identifier (article of the book).
    :param url_payment: Payment link.
    :param price: Product price.
    :param id_payment: Unique payment identifier.
    :return: The "pay_book" keyboard.
    """

    pay_book_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                pay_xtr_button(l10n, price=price),
            ],
            [
                pay_rub_button(l10n, price=price, url_payment=url_payment),
            ],
            [
                paid_book_button(
                    l10n=l10n,
                    id_book=id_book,
                    price=price,
                    id_payment=id_payment,
                ),
            ],
            [
                cancel_payment_button(l10n),
            ],
        ],
    )
    return pay_book_markup
