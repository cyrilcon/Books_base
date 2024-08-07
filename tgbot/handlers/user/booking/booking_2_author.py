from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.config import config
from tgbot.keyboards.inline import (
    cancel_keyboard,
    booking_again_keyboard,
    serve_unavailable_keyboard,
)
from tgbot.services import ClearKeyboard, create_user_link, get_user_language, Messenger
from tgbot.states import Booking

booking_router_2 = Router()


@booking_router_2.callback_query(StateFilter(Booking.send_author), F.data == "back")
async def back_to_booking_1(
    call: CallbackQuery, l10n: FluentLocalization, state: FSMContext
):
    """
    Going back to indicating the title of the book.
    :param call: Pressed "Back" button.
    :param l10n: Language set by the user.
    :param state: FSM (Booking).
    """

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("booking-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Booking.send_title)


@booking_router_2.message(StateFilter(Booking.send_author))
async def booking_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    """
    Adding an order.
    :param message: Message with expected author.
    :param l10n: Language set by the user.
    :param state: FSM (Booking).
    :param storage: Storage for FSM.
    :param bot: Bot instance.
    :return: Successful order message.
    """

    await ClearKeyboard.clear(message, storage)

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username

    author = message.text

    if len(author) <= 255:
        current_time = datetime.now()
        microseconds = current_time.microsecond
        id_booking = int(f"{str(id_user)[0]}{str(microseconds)[1:4]}{str(id_user)[-1]}")

        data = await state.get_data()
        title = data["title"]

        await api.bookings.create_booking(id_booking, id_user, title, author)

        await message.answer(
            l10n.format_value(
                "booking-success",
                {"title": title, "author": author, "id_booking": str(id_booking)},
            ),
            reply_markup=booking_again_keyboard(l10n),
        )
        await state.clear()

        user_link = await create_user_link(fullname, username)

        booking_information = l10n.format_value(
            "booking-information",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "title": title,
                "author": author,
                "id_booking": str(id_booking),
            },
        )
        text = l10n.format_value(
            "booking-from-user",
            {
                "booking_information": booking_information,
            },
        )
        language_code = await get_user_language(config.tg_bot.super_admin)
        await Messenger.safe_send_message(
            bot=bot,
            user_id=config.tg_bot.booking_chat,
            text=text,
            reply_markup=serve_unavailable_keyboard(language_code, id_booking),
        )
    else:
        sent_message = await message.answer(
            l10n.format_value("booking-author-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            user_id=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
