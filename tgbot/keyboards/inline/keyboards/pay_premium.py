from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline.buttons import pay_button, paid_button


def pay_premium_keyboard(
    l10n: FluentLocalization,
    url_payment: str,
    price: int | float,
    id_payment: str,
):
    """
    The "pay_premium" keyboard is formed.
    :param l10n: Language set by the user.
    :param url_payment: Payment link.
    :param price: Product price.
    :param id_payment: Unique payment identifier.
    :return: The "pay_premium" keyboard.
    """

    pay_premium_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"⭐ Оплатить 200 ⭐",
                    pay=True,
                ),
            ],
            [
                pay_button(l10n, price=price, url_payment=url_payment),
            ],
            [
                paid_button(l10n, price=price, id_payment=id_payment),
            ],
        ],
    )
    return pay_premium_markup
