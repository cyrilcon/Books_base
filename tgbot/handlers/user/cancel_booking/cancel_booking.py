from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
)
from tgbot.services import (
    get_user_language,
)
from tgbot.states import CancelBooking

cancel_booking_router = Router()


@cancel_booking_router.message(Command("cancel_booking"))
async def cancel_booking(message: Message, state: FSMContext):
    """
    Обработка команды /cancel_booking.
    :param message: Команда /cancel_booking.
    :param state: FSM (CancelBooking).
    :return: Сообщение для отмены заказа и переход в FSM (select_booking).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("cancel-booking-select"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(CancelBooking.select_booking)


@cancel_booking_router.message(StateFilter(CancelBooking.select_booking))
async def cancel_booking_process(message: Message, bot: Bot, state: FSMContext):
    """
    Отмена заказа.
    :param message: Сообщение с ожидаемым номером заказа.
    :param bot: Экземпляр бота.
    :param state: FSM (CancelBooking).
    :return: Сообщение для указания номера заказа и переход в FSM (select_booking).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    booking_number = message.text

    if booking_number[0] == "№":
        booking_number = booking_number[1:]

    if booking_number.isdigit():
        id_booking = int(booking_number)

        response = await api.bookings.get_booking(id_booking)
        status = response.status
        booking = response.result

        if status == 200 and booking["id_user"] == id_user:
            await api.bookings.delete_booking(id_booking)

            await state.clear()
            await message.answer(
                l10n.format_value(
                    "cancel-booking-completed",
                    {"id_booking": str(id_booking), "title": booking["title"]},
                ),
            )
        else:
            await message.answer(
                l10n.format_value("cancel-booking-does-not-exist"),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        await message.answer(
            l10n.format_value("cancel-booking-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
