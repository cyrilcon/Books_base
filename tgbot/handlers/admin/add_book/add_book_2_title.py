from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
    back_yes_cancel_keyboard,
)
from tgbot.services import ClearKeyboard
from tgbot.states import AddBook

add_book_router_2 = Router()
add_book_router_2.message.filter(AdminFilter())


@add_book_router_2.callback_query(StateFilter(AddBook.add_title), F.data == "back")
async def back_to_add_book_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    response = await api.books.get_latest_article()
    latest_article = response.result
    free_article = "#{:04d}".format(latest_article + 1)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value(
            "add-book-article",
            {"free_article": free_article},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.select_article)


@add_book_router_2.message(StateFilter(AddBook.add_title), F.text)
async def add_book_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    title = message.text

    if len(title) <= 255:
        if '"' in title:
            sent_message = await message.answer(
                l10n.format_value("add-book-title-incorrect"),
                reply_markup=back_cancel_keyboard(l10n),
            )
        else:
            response = await api.books.search_books_by_title(
                title, similarity_threshold=100
            )
            result = response.result
            found = result["found"]

            if found > 0:
                book = result["books"][0]["book"]
                sent_message = await message.answer(
                    l10n.format_value(
                        "add-book-title-already-exists",
                        {
                            "title": title,
                            "article": "#{:04d}".format(book["id_book"] + 1),
                        },
                    ),
                    reply_markup=back_yes_cancel_keyboard(l10n),
                )
            else:
                sent_message = await message.answer(
                    l10n.format_value("add-book-authors"),
                    reply_markup=back_cancel_keyboard(l10n),
                )
                await state.set_state(AddBook.add_authors)

            await state.update_data(title=title)
    else:
        sent_message = await message.answer(
            l10n.format_value("add-book-title-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_book_router_2.callback_query(StateFilter(AddBook.add_title), F.data == "yes")
async def yes_add_book_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-authors"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)
