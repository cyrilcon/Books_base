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

edit_book_4_description_router = Router()
edit_book_4_description_router.message.filter(IsPrivate())


@edit_book_4_description_router.callback_query(F.data.startswith("edit_description"))
async def edit_description(call: CallbackQuery, state: FSMContext):
    """
    Обработка кнопки "Описание".
    :param call: Кнопка "Описание".
    :param state: FSM (EditBook).
    :return: Сообщение для изменения описания книги и переход в FSM (edit_description).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    id_book = int(call.data.split(":")[-1])

    response = await api.books.get_book(id_book)
    book = response.result

    await call.message.answer(
        l10n.format_value(
            "edit-book-description",
            {"description": f"<code>{book["description"]}</code>"},
        ),
        reply_markup=cancel_keyboard(l10n),
    )

    await state.update_data(id_edit_book=id_book)
    await state.set_state(EditBook.edit_description)


@edit_book_4_description_router.message(StateFilter(EditBook.edit_description))
async def edit_description_process(
    message: Message, bot: Bot, state: FSMContext, config: Config
):
    """
    Изменение описания книги.
    :param message: Сообщение с ожидаемым описанием книги.
    :param bot: Экземпляр бота.
    :param state: FSM (EditBook).
    :param config: Config с параметрами бота.
    :return: Сообщение об успешном изменении описания.
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    description = message.text

    if len(description) > 850:
        await message.answer(
            l10n.format_value("edit-book-description-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
    else:
        data = await state.get_data()
        id_edit_book = data.get("id_edit_book")

        response = await api.books.update_book(id_edit_book, description=description)
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
