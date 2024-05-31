from aiogram import Router, F
from aiogram.types import CallbackQuery

from infrastructure.books_base_api import api
from tgbot.keyboards.inline import (
    confirm_exchange_keyboard,
)
from tgbot.services import (
    get_user_language,
)

base_store_exchange_router = Router()


@base_store_exchange_router.callback_query(F.data.startswith("discount"))
async def base_store_exchange(call: CallbackQuery):
    """
    Процесс обмена base на скидку.
    :param call: Нажатая кнопка со скидкой.
    :return: Сообщение для подтверждения обмена.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    discount = int(call.data.split(":")[-2])
    price = int(call.data.split(":")[-1])

    response = await api.users.get_user(id_user)
    bases = response.result["base"]

    residue = bases - price

    # Если у пользователя останется base меньше нуля
    if residue < 0:
        await call.answer(l10n.format_value("not-enough-bases"), show_alert=True)

    # Если у пользователя останется base
    else:
        discount_text = get_text_from_discount(l10n, discount)

        await call.answer(cache_time=1)
        await call.message.edit_text(
            l10n.format_value(
                "confirm-exchange",
                {
                    "price": str(price),
                    "discount_text": discount_text,
                    "residue": residue,
                },
            ),
            reply_markup=confirm_exchange_keyboard(l10n, discount, price),
        )


@base_store_exchange_router.callback_query(F.data.startswith("confirm-exchange"))
async def confirm_exchange(call: CallbackQuery):
    """
    Подтверждение обмена base на скидку.
    :param call: Нажатая кнопка со "Обменять".
    :return: Сообщение об успешном обмене.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    response = await api.users.get_premium(id_user)
    status = response.status

    # Если пользователь имеет PREMIUM
    if status == 200:
        await call.answer(l10n.format_value("user-has-premium"), show_alert=True)

    # Если пользователь не имеет PREMIUM
    else:
        response = await api.users.get_discount(id_user)
        status = response.status

        # Если пользователь имеет какую-либо скидку
        if status == 200:
            discount = response.result["discount"]

            # Если пользователь имеет 100% скидку
            if discount == 100:
                await call.answer(
                    l10n.format_value("user-has-free-book"), show_alert=True
                )

            # Если пользователь имеет любую другую скидку
            else:
                await call.answer(
                    l10n.format_value("user-has-discount", {"discount": discount}),
                    show_alert=True,
                )

        # Если пользователь не имеет никакую скидку
        else:
            discount = int(call.data.split(":")[-2])
            price = int(call.data.split(":")[-1])

            response = await api.users.get_user(id_user)
            bases = response.result["base"]

            residue = bases - price

            # Если у пользователя останется base меньше нуля
            if residue < 0:
                await call.answer(l10n.format_value("not-enough-base"), show_alert=True)

            # Если у пользователя останется base
            else:
                await api.users.update_user(id_user, base=residue)
                await api.users.create_discount(id_user, discount)

                discount_text = get_text_from_discount(l10n, discount)

                await call.answer(
                    l10n.format_value(
                        "exchange-completed-notification-window",
                        {"price": price, "discount_text": discount_text},
                    ),
                    show_alert=True,
                )
                await call.message.edit_text(
                    l10n.format_value(
                        "exchange-completed",
                        {
                            "price": price,
                            "discount_text": discount_text,
                            "residue": residue,
                        },
                    )
                )


def get_text_from_discount(l10n, discount: int) -> str:
    """
    Формирует текст в зависимости от скидки, которую имеет пользователь
    :param l10n: Язык установленный у пользователя.
    :param discount: Скидка пользователя.
    :return: Текст в зависимости от скидки.
    """

    if discount == 15:
        discount_text = l10n.format_value("discount-15")
    elif discount == 30:
        discount_text = l10n.format_value("discount-30")
    elif discount == 50:
        discount_text = l10n.format_value("discount-50")
    else:
        discount_text = l10n.format_value("discount-100")

    return discount_text
