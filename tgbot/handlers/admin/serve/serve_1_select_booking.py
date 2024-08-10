from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tgbot.services import ClearKeyboard, create_user_link
from tgbot.states import Serve

serve_router_1 = Router()
serve_router_1.message.filter(AdminFilter())


@serve_router_1.message(Command("serve"))
async def serve_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("serve-select-booking"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Serve.select_booking)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@serve_router_1.message(StateFilter(Serve.select_booking), F.text)
async def serve_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    booking_number = message.text

    if booking_number[0] == "№":
        booking_number = booking_number[1:]

    if booking_number.isdigit():
        id_booking = int(booking_number)

        response = await api.bookings.get_booking_by_id(id_booking)
        status = response.status
        booking = response.result

        if status == 200:
            response = await api.users.get_user_by_id(booking["id_user"])
            user = response.result
            id_user = user["id_user"]

            user_link = await create_user_link(user["fullname"], user["username"])

            sent_message = await message.answer(
                l10n.format_value(
                    "serve-send-book",
                    {
                        "user_link": user_link,
                        "id_user": str(id_user),
                        "title": booking["title"],
                        "author": booking["author"],
                        "id_booking": str(id_booking),
                    },
                ),
                reply_markup=back_cancel_keyboard(l10n),
            )
            await state.update_data(id_booking=id_booking)
            await state.set_state(Serve.send_book)
        else:
            sent_message = await message.answer(
                l10n.format_value("booking-not-found"),
                reply_markup=cancel_keyboard(l10n),
            )
    else:
        sent_message = await message.answer(
            l10n.format_value("booking-incorrect"),
            reply_markup=cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
