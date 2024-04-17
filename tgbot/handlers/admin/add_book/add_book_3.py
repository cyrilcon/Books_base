from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.keyboards import delete_keyboard
from tgbot.keyboards.inline import back_and_cancel_buttons
from tgbot.services import get_user_language
from tgbot.states import AddBook

add_book_router_3 = Router()
add_book_router_3.message.filter(AdminFilter())


@add_book_router_3.callback_query(
    StateFilter(AddBook.add_authors), F.data == "BACK_and_cancel"
)
async def back_to_add_book_2(call: CallbackQuery, state: FSMContext):
    """
    Возвращение назад к добавлению названия книги.
    :param call: Нажатая кнопка "« Назад".
    :param state: FSM (AddBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)

    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-name-book"),
        reply_markup=back_and_cancel_buttons,
    )
    await state.set_state(AddBook.add_title)


@add_book_router_3.message(StateFilter(AddBook.add_authors))
async def add_book_3(message: Message, bot: Bot, state: FSMContext):
    """
    Добавление автора(ов).
    :param message: Сообщение с ожидаемым(и) автором(ами).
    :param bot: Экземпляр бота.
    :param state: FSM (AddBook).
    :return: Сообщение для добавления описания и переход в FSM (add_authors).
    """

    await delete_keyboard(bot, message)

    id_user = message.from_user.id
    l10n = await get_user_language(id_user)

    authors = message.text.lower().split(", ")

    await message.answer(
        l10n.format_value("add-book-description"),
        reply_markup=back_and_cancel_buttons,
    )
    await state.update_data(authors=authors)
    await state.set_state(AddBook.add_description)
