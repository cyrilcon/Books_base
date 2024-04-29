from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.services import get_user_language
from tgbot.states import EditBook

update_book_cancel_router = Router()
update_book_cancel_router.message.filter(AdminFilter())


@update_book_cancel_router.callback_query(StateFilter(EditBook), F.data == "cancel")
async def update_book_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена изменения книги.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (UpdateBook).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value("update-book-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    try:
        await call.message.edit_text(text)
    except TelegramBadRequest:
        await call.message.edit_reply_markup()
