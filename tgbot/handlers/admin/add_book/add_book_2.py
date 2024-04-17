from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_button
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

    id_user = call.message.chat.id
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


# @add_book_router_2.message(Command("add_book"))
# async def add_book_2(message: Message, state: FSMContext):
#     """
#     Обработка команды /add_book_1.
#     :param message: Команда /add_book_1.
#     :param state: FSM (AddBook).
#     :return: Сообщение для выбора артикула и переход в FSM (select_article).
#     """
#
#     language = message.from_user.language_code
#     l10n = get_fluent_localization(language)
#
#     status, latest_article = await api.books.get_latest_article()
#     free_article = "#{:04d}".format(latest_article["latest_article"] + 1)
#
#     await message.answer(
#         l10n.format_value("add-book-article", {"free_article": free_article}),
#         reply_markup=cancel_button,
#     )
#
#     await state.set_state(AddBook.select_article)  # Вход в FSM (select_article)
