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
)
from tgbot.services import (
    get_user_language,
    levenshtein_search_one_book,
    forming_text,
    safe_send_message,
)
from tgbot.states import Booking

booking_router_1 = Router()


@booking_router_1.message(Command("booking"))
async def booking_1(message: Message, state: FSMContext):
    """
    Обработка команды /booking.
    :param message: Команда /booking.
    :param state: FSM (Booking).
    :return: Сообщение для написания названия книги и переход в FSM (send_title).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("booking-title"),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(Booking.send_title)


@booking_router_1.message(StateFilter(Booking.send_title))
async def booking_1_process(message: Message, bot: Bot, state: FSMContext):
    """
    Указание названия книги.
    :param message: Сообщение с ожидаемым названием книги.
    :param bot: Экземпляр бота.
    :param state: FSM (Booking).
    :return: Сообщение для указания автора книги и переход в FSM (send_author).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    title_from_message = message.text

    if len(title_from_message) < 255:
        response = await api.books.get_all_titles()
        all_titles = response.result

        founded_title = await levenshtein_search_one_book(
            title_from_message, all_titles
        )

        if founded_title:
            response = await api.books.get_book_by_title(founded_title)
            status = response.status
            books = response.result

            if status == 200:
                id_book = books["id_book"]
                title = books["title"]
                authors = ", ".join(
                    [author["author"].title() for author in books["authors"]]
                )
                article = "#{:04d}".format(id_book)

                await message.answer(
                    l10n.format_value(
                        "booking-title-already-exists",
                        {"title": title, "authors": authors, "article": article},
                    ),
                    reply_markup=show_booking_cancel_keyboard(l10n, id_book),
                )
        else:
            await message.answer(
                l10n.format_value("booking-author"),
                reply_markup=back_and_cancel_keyboard(l10n),
            )
            await state.set_state(Booking.send_author)
        await state.update_data(title=title_from_message)
    else:
        await message.answer(
            l10n.format_value("booking-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )


@booking_router_1.callback_query(StateFilter(Booking.send_title), F.data == "booking")
async def booking_1_booking(call: CallbackQuery, state: FSMContext):
    """
    Всё равно заказать книгу с таким названием.
    :param call: Нажатая кнопка "Всё равно заказать".
    :param state: FSM (Booking).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.message.edit_text(
        l10n.format_value("booking-author"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )
    await state.set_state(Booking.send_author)


@booking_router_1.callback_query(
    StateFilter(Booking.send_title), F.data.startswith("show_book")
)
async def booking_1_show_book(
    call: CallbackQuery, bot: Bot, state: FSMContext, config: Config
):
    """
    Просмотр книги.
    :param call: Нажатая кнопка "Показать книгу".
    :param bot: Экземпляр бота.
    :param state: FSM (Booking).
    :param config: Config с параметрами бота.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_reply_markup()
    await state.clear()

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book(id_book)
    status = response.status
    book = response.result

    if status == 200:
        post_text = await forming_text(book, l10n)

        await safe_send_message(
            config=config,
            bot=bot,
            id_user=id_user,
            text=post_text,
            photo=book["cover"],
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
