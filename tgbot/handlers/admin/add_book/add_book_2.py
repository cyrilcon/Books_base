from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import cancel_button, back_and_cancel_buttons
from tgbot.services import get_fluent_localization
from tgbot.states import AddBook

add_book_router_2 = Router()
add_book_router_2.message.filter(AdminFilter())


@add_book_router_2.callback_query(
    StateFilter(AddBook.add_name_book), F.data == "BACK_and_cancel"
)
async def back_to_add_book_1(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к выбору артикула.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    status, user = await api.users.get_user(id_user)
    language = user["language"]
    l10n = get_fluent_localization(language)

    status, latest_article = await api.books.get_latest_article()
    free_article = "#{:04d}".format(latest_article["latest_article"] + 1)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-article", {"free_article": free_article}),
        reply_markup=cancel_button,
    )
    await state.set_state(AddBook.select_article)  # Вход в FSM (select_article)


@add_book_router_2.message(StateFilter(AddBook.add_name_book))
async def add_book_2(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление названия книги.
    :param message: Сообщение с ожидаемым названием книги.
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для выбора автора и переход в FSM (add_author).
    """

    await delete_keyboard(bot, message)  # Удаляются inline кнопки

    id_user = message.from_user.id
    status, user = await api.users.get_user(id_user)
    language = user["language"]
    l10n = get_fluent_localization(language)

    name_book = message.text  # Название книги

    if "#" in name_book:
        await message.answer(
            l10n.format_value("add-book-name-book-incorrect"),
            reply_markup=back_and_cancel_buttons,
        )
    else:
        await message.answer(
            l10n.format_value("add-book-author"),
            reply_markup=back_and_cancel_buttons,
        )
        await state.update_data(name_book=name_book)  # Сохраняется название книги

    await state.set_state(AddBook.add_author)  # Вход в FSM (add_author)
