from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.filters.private_chat import IsPrivate
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import (
    cancel_keyboard,
    edit_keyboard,
)
from tgbot.services import get_user_language, forming_text, send_message
from tgbot.states import EditBook

edit_book_6_cover_router = Router()
edit_book_6_cover_router.message.filter(IsPrivate())


@edit_book_6_cover_router.callback_query(F.data.startswith("edit_cover"))
async def edit_cover(call: CallbackQuery, bot: Bot, state: FSMContext, config: Config):
    """
    Обработка кнопки "Обложка".
    :param call: Кнопка "Обложка".
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение для изменения обложки книги и переход в FSM (edit_cover).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book(id_book)
    book = response.result

    await send_message(
        config=config,
        bot=bot,
        id_user=id_user,
        text=l10n.format_value("edit-book-cover"),
        photo=book["cover"],
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_cover)


@edit_book_6_cover_router.message(StateFilter(EditBook.edit_cover), F.photo)
async def edit_cover_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Изменение обложки книги.
    :param message: Сообщение с ожидаемой фотографией обложки.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении обложки.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    cover = message.photo[-1].file_id

    data = await state.get_data()
    id_edit_book = data.get("id_edit_book")

    response = await api.books.update_book(id_edit_book, cover=cover)
    status = response.status
    book = response.result

    if status == 200:
        post_text = await forming_text(book, l10n)

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
