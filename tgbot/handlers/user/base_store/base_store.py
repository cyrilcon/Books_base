from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.keyboards.inline import (
    exchange_base_keyboard,
    discounts_keyboard,
)
from tgbot.services import (
    get_user_language,
)

base_store_router = Router()


@base_store_router.message(Command("base_store"))
async def base_store(message: Message):
    """
    Обработка команды /base_store.
    :param message: Команда /base_store.
    :return: Приветственное сообщение Base_store.
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    response = await api.users.get_premium(id_user)
    status = response.status

    # Если пользователь имеет PREMIUM
    if status == 200:
        account_information = l10n.format_value("user-has-premium")
        await message.answer(
            l10n.format_value(
                "welcome-to-base-store",
                {"account_information": f"<i>{account_information}</i>"},
            )
        )

    # Если пользователь не имеет PREMIUM
    else:
        response = await api.users.get_discount(id_user)
        status = response.status

        # Если пользователь имеет какую-либо скидку
        if status == 200:
            discount = response.result["discount"]

            # Если пользователь имеет 100% скидку
            if discount == 100:
                discount_of_user = l10n.format_value("user-has-free-book") + "\n\n"

            # Если пользователь имеет любую другую скидку
            else:
                discount_of_user = (
                    l10n.format_value("user-has-discount", {"discount": discount})
                    + "\n\n"
                )
            keyboard = None

        # Если пользователь не имеет никакую скидку
        else:
            discount_of_user = ""
            keyboard = exchange_base_keyboard(l10n)

        response = await api.users.get_user(id_user)
        bases = response.result["base"]

        amount_base = l10n.format_value(
            "base-store-account-amount-base",
            {"bases": bases},
        )

        account_information = f"<i>{discount_of_user}</i>" + amount_base

        await message.answer(
            l10n.format_value(
                "welcome-to-base-store",
                {"account_information": account_information},
            ),
            reply_markup=keyboard,
        )


@base_store_router.callback_query(F.data.in_({"exchange", "back-to-exchange"}))
async def exchange(call: CallbackQuery):
    """
    Обмен base на скидки.
    :param call: Нажатая кнопка "💎 Обменять 💎" или "« Назад".
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    response = await api.users.get_user(id_user)
    bases = response.result["base"]

    amount_base = l10n.format_value("base-store-account-amount-base", {"bases": bases})

    await call.message.edit_text(
        l10n.format_value("exchange-bases", {"amount_base": amount_base}),
        reply_markup=discounts_keyboard(l10n),
    )
