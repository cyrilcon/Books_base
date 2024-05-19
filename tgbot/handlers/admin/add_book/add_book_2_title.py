from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    back_and_cancel_keyboard,
    yes_and_cancel_keyboard,
)
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_2 = Router()
add_book_router_2.message.filter(AdminFilter())


@add_book_router_2.callback_query(StateFilter(AddBook.add_title), F.data == "back")
async def back_to_add_book_1(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к выбору артикула.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    response = await api.books.get_latest_article()
    latest_article = response.result
    free_article = "#{:04d}".format(latest_article + 1)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-article", {"free_article": free_article}),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.select_article)


@add_book_router_2.message(StateFilter(AddBook.add_title))
async def add_book_2(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление названия книги.
    :param message: Сообщение с ожидаемым названием книги.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления автора(ов) и переход в FSM (add_description).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    title = message.text

    if len(title) > 250:
        await message.answer(
            l10n.format_value("add-book-title-too-long"),
            reply_markup=back_and_cancel_keyboard(l10n),
        )
    else:
        if any(char in title for char in {"#", '"'}):
            await message.answer(
                l10n.format_value("add-book-title-incorrect"),
                reply_markup=back_and_cancel_keyboard(l10n),
            )
        else:
            response = await api.books.get_book_by_title(title)
            status = response.status
            book = response.result

            if status == 200:
                await message.answer(
                    l10n.format_value(
                        "add-book-title-already-exists",
                        {
                            "title": title,
                            "article": "#{:04d}".format(book["id_book"] + 1),
                        },
                    ),
                    reply_markup=yes_and_cancel_keyboard(l10n),
                )
            else:
                await message.answer(
                    l10n.format_value("add-book-authors"),
                    reply_markup=back_and_cancel_keyboard(l10n),
                )
                await state.update_data(title=title)
                await state.set_state(AddBook.add_authors)


@add_book_router_2.callback_query(StateFilter(AddBook.add_title), F.data == "yes")
async def yes_add_book_2(call: CallbackQuery, state: FSMContext):
    """
    Подтверждение добавления названия.
    :param call: Нажатая кнопка "Да".
    :param state: FSM (AddBook).
    :return: Сообщение для добавления автора(ов) и переход в FSM (add_description).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-authors"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)
