import re

from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from infrastructure.books_base_api import api
from tgbot.filters.private_chat import IsPrivate
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import get_user_language
from tgbot.states import EditBook

edit_book_1_article_router = Router()
edit_book_1_article_router.message.filter(IsPrivate())


@edit_book_1_article_router.callback_query(F.data.startswith("edit_article"))
async def edit_article(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопок "Артикул".
    :param call: Кнопка "Артикул".
    :param state: FSM (EditBook).
    :return: Сообщение для выбора артикула и переход в FSM (edit_article).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    id_book = int(call.data.split(":")[-1])
    article = "#{:04d}".format(id_book)

    await call.message.answer(
        l10n.format_value("edit-book-article", {"article": article}),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.set_state(EditBook.edit_article)


@edit_book_1_article_router.message(StateFilter(EditBook.edit_article))
async def edit_article_process(message: Message, bot: Bot, state: FSMContext):
    """
    Изменение артикула книги.
    :param message: Сообщение с ожидаемым артикулом книги.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :return: Сообщение об успешном изменении артикула.
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

        if status == 200:
            await message.answer(
                l10n.format_value("edit-book-article-already-exist"),
                reply_markup=cancel_keyboard(l10n),
            )
        else:
            # TODO: Реализовать обновление данных о книге
            # response = await api.books.update_book(id_book, id_book=id_book)

            await message.answer(
                l10n.format_value("edit-book-article-successfully-changed")
            )

            await state.clear()
