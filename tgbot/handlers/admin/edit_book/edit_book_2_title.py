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
    yes_and_cancel_keyboard,
)
from tgbot.services import get_user_language, forming_text, send_message
from tgbot.states import EditBook

edit_book_router_2 = Router()
edit_book_router_2.message.filter(AdminFilter())


@edit_book_router_2.callback_query(F.data.startswith("edit_title"))
async def edit_title(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопки "Название".
    :param call: Кнопка "Название".
    :param state: FSM (EditBook).
    :return: Сообщение для изменения названия книги и переход в FSM (edit_title).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    id_book = int(call.data.split(":")[-1])
    response = await api.books.get_book(id_book)
    book = response.result

    await call.message.answer(
        l10n.format_value("edit-book-title", {"title": book["title"]}),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_title)


@edit_book_router_2.message(StateFilter(EditBook.edit_title))
async def edit_title_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Изменение названия книги.
    :param message: Сообщение с ожидаемым названием книги.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении названия.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    title = message.text

    if len(title) > 250:
        await message.answer(
            l10n.format_value("edit-book-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        if any(char in title for char in {"#", '"'}):
            await message.answer(
                l10n.format_value("add-book-title-incorrect"),
                reply_markup=cancel_keyboard(l10n),
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
                await state.update_data(title=title)
            else:
                data = await state.get_data()
                id_edit_book = data.get("id_edit_book")

                response = await api.books.update_book(id_edit_book, title=title)
                status = response.status
                book = response.result

                if status == 200:
                    post_text = await forming_text(book, l10n)
                    post_text_length = len(post_text)

                    if post_text_length <= 1000:
                        await message.answer(
                            l10n.format_value("edit-book-successfully-changed")
                        )
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


@edit_book_router_2.callback_query(StateFilter(EditBook.edit_title), F.data == "yes")
async def yes_edit_title(
    call: CallbackQuery, bot: Bot, state: FSMContext, config: Config
):
    """
    Подтверждение изменения названия.
    :param call: Нажатая кнопка "Да".
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении названия.
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)

    data = await state.get_data()
    id_edit_book = data.get("id_edit_book")
    title = data.get("title")

    response = await api.books.update_book(id_edit_book, title=title)
    status = response.status
    book = response.result

    if status == 200:
        await call.message.edit_text(
            l10n.format_value("edit-book-successfully-changed")
        )

        post_text = await forming_text(book, l10n)

        await send_message(
            config=config,
            bot=bot,
            id_user=id_user,
            text=post_text,
            photo=book["cover"],
            reply_markup=edit_keyboard(l10n, book["id_book"]),
        )

    await state.clear()
