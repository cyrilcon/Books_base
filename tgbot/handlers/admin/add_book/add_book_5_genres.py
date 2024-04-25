import re

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    back_and_cancel_keyboard,
    ready_clear_back_cancel_keyboard,
)
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_5 = Router()
add_book_router_5.message.filter(AdminFilter())


@add_book_router_5.callback_query(StateFilter(AddBook.add_genres), F.data == "back")
async def back_to_add_book_4(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к добавлению описания.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-description"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_description)


@add_book_router_5.message(StateFilter(AddBook.add_genres))
async def add_book_5(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление жанров.
    :param message: Сообщение с ожидаемыми жанрами.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления обложки и переход в FSM (add_cover).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    genres_from_message = message.text

    data = await state.get_data()
    genres = data.get("genres")

    genres = await genres_to_list(genres_from_message, genres)
    await state.update_data(genres=genres)
    ready_made_genres = " ".join(["#" + genre["genre"] for genre in genres])

    await message.answer(
        l10n.format_value(
            "add-book-genres-example",
            {"ready_made_genres": ready_made_genres},
        ),
        reply_markup=ready_clear_back_cancel_keyboard(l10n),
    )


@add_book_router_5.callback_query(StateFilter(AddBook.add_genres), F.data == "done")
async def done_add_book_5(call: CallbackQuery, state: FSMContext):
    """
    Добавление обложки.
    :param call: Нажатая кнопка "Готово".
    :param state: FSM (AddBook).
    :return: Сообщение для добавления обложки и переход в FSM (add_cover).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.message.edit_text(
        l10n.format_value("add-book-cover"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_cover)


@add_book_router_5.callback_query(StateFilter(AddBook.add_genres), F.data == "clear")
async def clear_add_book_5(call: CallbackQuery, state: FSMContext):
    """
    Очистка списка всех жанров.
    :param call: Нажатая кнопка "Стереть".
    :param state: FSM (AddBook).
    :return: Сообщение для добавления жанров сначала
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.message.edit_text(
        l10n.format_value("add-book-genres"),
        reply_markup=back_and_cancel_keyboard(l10n),
    )
    genres = []
    await state.update_data(genres=genres)


async def genres_to_list(
    genres_from_message: str, genres: list[str] = None
) -> list[dict]:
    """
    Превращает жанры в список.
    :param genres_from_message: Жанры книг.
    :param genres: Список с уже записанными жанрами.
    :return: Список с жанрами.
    """

    if genres is None:
        genres = []

    new_genres = re.findall(r"\b(\w+(?:\s+\w+)*)\b", genres_from_message)
    new_genres = [
        {"genre": genre.strip().replace(" ", "_").lower()} for genre in new_genres
    ]

    for genre in new_genres:
        if genre["genre"] not in [g["genre"] for g in genres]:
            genres.append(genre)

    return genres
