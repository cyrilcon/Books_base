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

edit_book_3_authors_router = Router()
edit_book_3_authors_router.message.filter(AdminFilter())


@edit_book_3_authors_router.callback_query(F.data.startswith("edit_authors"))
async def edit_authors(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопки "Авторы".
    :param call: Кнопка "Авторы".
    :param state: FSM (EditBook).
    :return: Сообщение для изменения авторов книги и переход в FSM (edit_authors).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book(id_book)
    book = response.result

    authors = ", ".join([author["author"].title() for author in book["authors"]])

    await call.message.answer(
        l10n.format_value("edit-book-authors", {"authors": f"<code>{authors}</code>"}),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_authors)


@edit_book_3_authors_router.message(StateFilter(EditBook.edit_authors))
async def edit_authors_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Изменение автора(ов) книги.
    :param message: Сообщение с ожидаемым автором книги.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении автора.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    authors = message.text.lower().split(", ")
    authors = [{"author": author} for author in authors]

    data = await state.get_data()
    id_edit_book = data.get("id_edit_book")

    response = await api.books.update_book(id_edit_book, authors=authors)
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
