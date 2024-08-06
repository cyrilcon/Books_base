from typing import Tuple, Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import check_booking_keyboard
from tgbot.services import create_user_link

check_booking_router = Router()
check_booking_router.message.filter(AdminFilter())


@check_booking_router.message(Command("check_booking"))
async def check_booking(message: Message, l10n: FluentLocalization):
    """
    Processing of the /check_booking command.
    :param message: /check_booking command.
    :param l10n: Language set by the user.
    :return: Message with incoming bookings.
    """

    text, booking_count = await get_booking_info(l10n)

    if booking_count == 0:
        await message.answer(l10n.format_value("booking-absent"))
    else:
        await message.answer(text, reply_markup=check_booking_keyboard(booking_count))


@check_booking_router.callback_query(F.data.startswith("booking_position"))
async def check_booking_flipping(call: CallbackQuery, l10n: FluentLocalization):
    """
    Handling forward and back buttons for viewing orders.
    :param call: Pressed "Back" or "Forward" button.
    :param l10n: Language set by the user.
    :return: Next or previous order page.
    """

    await call.answer(cache_time=1)
    position = int(call.data.split(":")[-1])

    text, booking_count = await get_booking_info(l10n, position=position)

    if booking_count == 0:
        await call.message.edit_text(l10n.format_value("booking-absent"))
    else:
        await call.message.edit_text(
            text, reply_markup=check_booking_keyboard(booking_count, position=position)
        )


async def get_booking_info(
    l10n: FluentLocalization, position: int = 1
) -> Tuple[Optional[str], int]:
    """
    Receive order information and total number of orders.

    :param l10n: Language set by the user.
    :param position: Order position among the total number of orders.
    :return: A tuple containing text with order information and the number of orders.
    """

    response = await api.bookings.get_booking_count()
    booking_count = response.result

    if booking_count == 0:
        return None, booking_count

    response = await api.bookings.get_booking_by_position(position)
    booking = response.result

    response = await api.users.get_user_by_id(booking["id_user"])
    user = response.result

    user_link = await create_user_link(user["fullname"], user["username"])

    text = l10n.format_value(
        "booking-information",
        {
            "user_link": user_link,
            "id_user": str(user["id_user"]),
            "title": booking["title"],
            "author": booking["author"],
            "id_booking": str(booking["id_booking"]),
        },
    )

    return text, booking_count
