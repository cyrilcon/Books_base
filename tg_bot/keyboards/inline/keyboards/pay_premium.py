from aiogram.types import InlineKeyboardMarkup
from fluent.runtime import FluentLocalization

from keyboards.inline.buttons.payment import cancel_payment_button
from tg_bot.keyboards.inline.buttons import pay_stars_button, pay_button, paid_button


def pay_premium_keyboard(
    l10n: FluentLocalization,
    url_payment: str,
    currency: str,
    price_stars: int,
    price_rub: int | float,
    id_payment: str,
):
    """
    The "pay_premium" keyboard is formed.
    :param l10n: Language set by the user.
    :param url_payment: Payment link.
    :param currency: Currency in which the payment was made.
    :param price_stars: Product price in stars.
    :param price_rub: Product price in rubles.
    :param id_payment: Unique payment identifier.
    :return: The "pay_premium" keyboard.
    """

    pay_premium_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                pay_stars_button(l10n, price=price_stars),
            ],
            [
                pay_button(l10n, price=price_rub, url_payment=url_payment),
            ],
            [
                paid_button(
                    l10n,
                    currency=currency,
                    price=price_rub,
                    id_payment=id_payment,
                ),
            ],
            [
                cancel_payment_button(l10n),
            ],
        ],
    )
    return pay_premium_markup
