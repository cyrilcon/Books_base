from typing import List

from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline.buttons import (
    pay_xtr_button,
    pay_rub_button,
    paid_set_button,
    cancel_payment_button,
)


def pay_set_keyboard(
    l10n: FluentLocalization,
    book_ids: List[int],
    url_payment: str,
    price_xtr: int,
    price_rub: int | float,
    id_payment: str,
):
    """
    The "pay_set" keyboard is formed.
    :param l10n: Language set by the user.
    :param book_ids: List of book ids.
    :param url_payment: Payment link.
    :param price_xtr: Product price in stars.
    :param price_rub: Product price in rubles.
    :param id_payment: Unique payment identifier.
    :return: The "pay_set" keyboard.
    """

    pay_set_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                pay_xtr_button(l10n, price=price_xtr),
            ],
            [
                pay_rub_button(l10n, price=price_rub, url_payment=url_payment),
            ],
            [
                paid_set_button(l10n, book_ids=book_ids, id_payment=id_payment),
            ],
            [
                cancel_payment_button(l10n),
            ],
        ],
    )
    return pay_set_markup
