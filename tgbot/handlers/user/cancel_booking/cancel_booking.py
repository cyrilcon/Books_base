from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.config import config
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import CancelBooking

cancel_booking_router = Router()


@cancel_booking_router.message(Command("cancel_booking"))
async def cancel_booking(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("cancel-booking-select"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(CancelBooking.select_booking)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@cancel_booking_router.message(StateFilter(CancelBooking.select_booking), F.text)
async def cancel_booking_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    booking_number = message.text
    id_user = message.from_user.id

    if booking_number[0] == "№":
        booking_number = booking_number[1:]

    if booking_number.isdigit():
        id_booking = int(booking_number)

        response = await api.orders.get_booking_by_id(id_booking)
        status = response.status
        booking = response.result

        if status == 200 and (
            id_user == config.tg_bot.super_admin or id_user == booking["id_user"]
        ):
            await api.orders.delete_booking(id_booking)

            await state.clear()
            await message.answer(
                l10n.format_value(
                    "cancel-booking-success",
                    {"id_booking": str(id_booking), "title": booking["title"]},
                ),
            )
        else:
            sent_message = await message.answer(
                l10n.format_value("booking-not-found"),
                reply_markup=cancel_keyboard(l10n),
            )
            await ClearKeyboard.safe_message(
                storage=storage,
                id_user=message.from_user.id,
                sent_message_id=sent_message.message_id,
            )
    else:
        sent_message = await message.answer(
            l10n.format_value("booking-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
