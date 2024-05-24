from datetime import datetime

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    booking_from_user_keyboard,
    booking_again_keyboard,
)
from tgbot.services import get_user_language, send_message, get_url_user
from tgbot.states import Booking

booking_router_2 = Router()


@booking_router_2.callback_query(StateFilter(Booking.send_author), F.data == "back")
async def back_to_booking_1(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к указанию названия книги.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (Booking).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("booking-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Booking.send_title)


@booking_router_2.message(StateFilter(Booking.send_author))
async def booking_2(message: Message, bot: Bot, state: FSMContext, config: Config):
    """
    Добавление заказа.
    :param message: Сообщение с ожидаемым автором.
    :param bot: Экземпляр бота.
    :param state: FSM (Booking).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном заказе.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    fullname = message.from_user.full_name
    username = message.from_user.username
    l10n = await get_user_language(id_user)

    author = message.text

    if len(author) < 255:
        current_time = datetime.now()
        microseconds = current_time.microsecond
        id_booking = int(f"{str(id_user)[0]}{str(microseconds)[1:4]}{str(id_user)[-1]}")

        data = await state.get_data()
        title = data["title"]

        await api.booking.create_booking(id_user, id_booking, title, author)

        await message.answer(
            l10n.format_value(
                "booking-complete",
                {"title": title, "author": author, "id_booking": str(id_booking)},
            ),
            reply_markup=booking_again_keyboard(l10n),
        )

        url_user = await get_url_user(fullname, username)

        text = l10n.format_value(
            "booking-from-user",
            {
                "url_user": url_user,
                "id_user": str(id_user),
                "title": title,
                "author": author,
                "id_booking": str(id_booking),
            },
        )

        await send_message(
            config=config,
            bot=bot,
            id_user=config.tg_bot.booking_chat,
            text=text,
            reply_markup=booking_from_user_keyboard(l10n),
        )

        await state.clear()
    else:
        await message.answer(
            l10n.format_value("booking-author-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
