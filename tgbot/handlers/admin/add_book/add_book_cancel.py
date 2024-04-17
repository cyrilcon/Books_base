from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from infrastructure.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.services import get_fluent_localization
from tgbot.states import AddBook

add_book_cancel_router = Router()
add_book_cancel_router.message.filter(AdminFilter())


@add_book_cancel_router.callback_query(
    StateFilter(AddBook), F.data == "back_and_CANCEL"
)
async def add_book_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена добавления книги.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (AddBook).
    """

    id_user = call.message.chat.id
    status, user = await api.users.get_user(id_user)
    language = user["language"]
    l10n = get_fluent_localization(language)
    text = l10n.format_value("add-book-cancel")

    await state.clear()  # Выход из FSM
    await call.answer(text, show_alert=True)  # Появляется окно с уведомлением
    await call.message.edit_text(text)
