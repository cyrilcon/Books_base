import re

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    edit_keyboard,
)
from tgbot.services import get_user_language, forming_text, send_message
from tgbot.states import EditBook

edit_book_router_5 = Router()
edit_book_router_5.message.filter(AdminFilter())


@edit_book_router_5.callback_query(F.data.startswith("edit_genres"))
async def edit_genres(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопки "Жанры".
    :param call: Кнопка "Жанры".
    :param state: FSM (EditBook).
    :return: Сообщение для изменения жанров книги и переход в FSM (edit_genres).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book(id_book)
    book = response.result

    genres = " ".join(["#" + genre["genre"] for genre in book["genres"]])

    await call.message.answer(
        l10n.format_value(
            "edit-book-genres",
            {"genres": f"<code>{genres}</code>"},
        ),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_genres)


@edit_book_router_5.message(StateFilter(EditBook.edit_genres))
async def edit_genres_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Изменение жанров книги.
    :param message: Сообщение с ожидаемыми жанрами книги.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении жанров.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    genres_message = message.text

    genres_list = re.findall(r"\b(\w+(?:\s+\w+)*)\b", genres_message)
    genres = [
        {"genre": genre.strip().replace(" ", "_").lower()} for genre in genres_list
    ]

    data = await state.get_data()
    id_edit_book = data.get("id_edit_book")

    response = await api.books.update_book(id_edit_book, genres=genres)
    status = response.status
    book = response.result

    if status == 200:
        post_text = await forming_text(book, l10n)
        post_text_length = len(post_text)

        if post_text_length <= 1000:
            await message.answer(l10n.format_value("edit-book-successfully-changed"))
            await send_message(
                config=config,
                bot=bot,
                id_user=id_user,
                text=post_text,
                photo=book["cover"],
                reply_markup=edit_keyboard(l10n, book["id_book"]),
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value(
                    "edit-book-too-long-text",
                    {
                        "post_text_length": post_text_length,
                    },
                ),
                reply_markup=cancel_keyboard(l10n),
            )
