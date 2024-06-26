from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import check_booking_pagination_keyboard
from tgbot.services import get_user_language, get_url_user

check_booking_router = Router()
check_booking_router.message.filter(AdminFilter())


@check_booking_router.message(Command("check_booking"))
async def check_booking(message: Message):
    """
    Обработка команды /check_booking.
    :param message: Команда /check_booking.
    :return: Сообщение c поступившими заказами.
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    text, booking_count = await get_booking_info(l10n, 1, id_user)

    if booking_count == 0:
        await message.answer(l10n.format_value("booking-absent"))
    else:
        await message.answer(
            text, reply_markup=check_booking_pagination_keyboard(1, booking_count)
        )


@check_booking_router.callback_query(F.data.startswith("booking_page"))
async def check_booking_flipping(call: CallbackQuery):
    """
    Обработка кнопок вперёд и назад для просмотра заказов.
    :param call: Кнопка вперёд или назад.
    :return: Следующую/предыдущую страницу заказа.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    page = int(call.data.split(":")[-1])

    text, booking_count = await get_booking_info(l10n, page, id_user)

    if booking_count == 0:
        await call.message.edit_text(l10n.format_value("booking-absent"))
    else:
        await call.message.edit_text(
            text, reply_markup=check_booking_pagination_keyboard(page, booking_count)
        )


async def get_booking_info(l10n, page: int, id_user: int):
    """
    Получение информации о заказе и общего количества заказов.

    :param l10n: Объект для локализации строк.
    :param page: Номер страницы (порядковый номер заказа).
    :param id_user: Идентификатор пользователя.
    :return: Кортеж, содержащий текст с информацией о заказе и количество заказов.
    """

    response = await api.bookings.get_booking_count()
    booking_count = response.result

    if booking_count == 0:
        return None, booking_count

    response = await api.bookings.get_booking_by_position(page)
    booking = response.result

    response = await api.users.get_user(booking["id_user"])
    user = response.result

    url_user = await get_url_user(user["fullname"], user["username"])
    text = l10n.format_value(
        "booking-information",
        {
            "url_user": url_user,
            "id_user": str(id_user),
            "title": booking["title"],
            "author": booking["author"],
            "id_booking": str(booking["id_booking"]),
        },
    )

    return text, booking_count
