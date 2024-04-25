from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_keyboard, back_and_cancel_keyboard
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

    status, latest_article = await api.books.get_latest_article()
    free_article = "#{:04d}".format(latest_article["latest_article"] + 1)

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

    if "#" in title:
        await message.answer(
            l10n.format_value("add-book-name-book-incorrect"),
            reply_markup=back_and_cancel_keyboard(l10n),
        )
    else:
        await message.answer(
            l10n.format_value("add-book-authors"),
            reply_markup=back_and_cancel_keyboard(l10n),
        )
        await state.update_data(title=title)
        await state.set_state(AddBook.add_authors)
