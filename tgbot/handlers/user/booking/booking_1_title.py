from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
    show_book_booking_cancel_keyboard,
)
from tgbot.services import ClearKeyboard, Messenger, generate_book_caption
from tgbot.states import Booking

booking_router_1 = Router()


@booking_router_1.message(Command("booking"))
async def booking_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("booking-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Booking.send_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@booking_router_1.message(StateFilter(Booking.send_title), F.text)
async def booking_1_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    title = message.text

    if len(title) <= 255:
        response = await api.books.search_books_by_title(
            title, similarity_threshold=100
        )
        result = response.result
        found = result["found"]

        if found > 0:
            book = result["books"][0]["book"]

            id_book = book["id_book"]
            title = book["title"]
            authors = ", ".join(
                [author["author"].title() for author in book["authors"]]
            )
            article = "#{:04d}".format(id_book)

            sent_message = await message.answer(
                l10n.format_value(
                    "booking-title-already-exists",
                    {"title": title, "authors": authors, "article": article},
                ),
                reply_markup=show_book_booking_cancel_keyboard(l10n, id_book),
            )
        else:
            sent_message = await message.answer(
                l10n.format_value("booking-author"),
                reply_markup=back_cancel_keyboard(l10n),
            )
            await state.set_state(Booking.send_author)
        await state.update_data(title=title)
    else:
        sent_message = await message.answer(
            l10n.format_value("title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@booking_router_1.callback_query(StateFilter(Booking.send_title), F.data == "booking")
async def booking_1_booking(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("booking-author"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(Booking.send_author)


@booking_router_1.callback_query(
    StateFilter(Booking.send_title), F.data.startswith("show_book")
)
async def booking_1_show_book(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    bot: Bot,
):
    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book_by_id(id_book)
    status = response.status

    if status == 200:
        await call.message.edit_reply_markup()
        await state.clear()

        book = response.result

        caption = await generate_book_caption(data=book, l10n=l10n)

        await Messenger.safe_send_message(
            bot=bot,
            user_id=call.from_user.id,
            text=caption,
            photo=book["cover"],
            # reply_markup=deep_link_buy_keyboard(deep_link),  # TODO: добавить кнопку "Купить"
        )
    else:
        await call.message.answer(
            l10n.format_value(
                "search-book-does-not-exist",
                {"article": "#{:04d}".format(int(id_book))},
            )
        )
