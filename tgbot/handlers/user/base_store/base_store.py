from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_and_cancel_keyboard,
    show_booking_cancel_keyboard,
    exchange_base_keyboard,
    discounts_keyboard,
)
from tgbot.services import (
    get_user_language,
    levenshtein_search_one_book,
    forming_text,
    send_message,
)
from tgbot.states import Booking

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

    response = await api.users.get_discount(id_user)
    status = response.status
    discount = response.result

    if status == 200:
        if discount == 100:
            discount_of_user = "\nУ вас действует купон на <b>бесплатную книгу</b>!!"
        else:
            discount_of_user = f"\nУ вас действует <b>скидка {discount}%</b>!!"
    else:
        discount_of_user = ""

    response = await api.users.get_bases(id_user)
    bases = response.result

    await message.answer(
        l10n.format_value(
            "welcome-to-base-store",
            {"discount_of_user": discount_of_user, "bases": bases},
        ),
        reply_markup=exchange_base_keyboard(l10n),
    )


@base_store_router.callback_query(F.data == "exchange")
async def exchange(call: CallbackQuery):
    """
    Обмен base на скидки.
    :param call: Нажатая кнопка "💎 Обменять 💎" или "« Назад".
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    response = await api.users.get_bases(id_user)
    bases = response.result

    await call.message.edit_text(
        l10n.format_value("exchange-bases", {"bases": bases}),
        reply_markup=discounts_keyboard(l10n),
    )
