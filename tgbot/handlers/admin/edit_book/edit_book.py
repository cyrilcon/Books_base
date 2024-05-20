import re

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.config import Config
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard, edit_keyboard
from tgbot.services import get_user_language, forming_text, send_message
from tgbot.states import EditBook

edit_book_router = Router()
edit_book_router.message.filter(AdminFilter())


@edit_book_router.message(Command("edit_book"))
async def edit_book(message: Message, state: FSMContext):
    """
    Обработка команды /edit_book.
    :param message: Команда /edit_book.
    :param state: FSM (EditBook).
    :return: Сообщение для выбора книги и переход в FSM (select_book).
    """

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    await message.answer(
        l10n.format_value("edit-book-select"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(EditBook.select_book)


@edit_book_router.message(StateFilter(EditBook.select_book))
async def edit_book_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Поиск книги по артикулу.
    :param message: Сообщение с ожидаемым артикулом книги.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Вся информация о книге и кнопки для изменения данных.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    article = message.text

    if not article.startswith("#") or not re.fullmatch(r"#\d{4}", article):
        await message.answer(
            l10n.format_value("edit-book-incorrect-article"),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        id_book = int(article[1:])

        response = await api.books.get_book(id_book)
        status = response.status
        book = response.result

        if status == 200:
            post_text = await forming_text(book, l10n)

            await send_message(
                config=config,
                bot=bot,
                id_user=id_user,
                text=post_text,
                photo=book["cover"],
                reply_markup=edit_keyboard(l10n, id_book),
            )
            await state.clear()
        else:
            await message.answer(
                l10n.format_value(
                    "edit-book-does-not-exist",
                    {"article": article},
                ),
                reply_markup=cancel_keyboard(l10n),
            )
