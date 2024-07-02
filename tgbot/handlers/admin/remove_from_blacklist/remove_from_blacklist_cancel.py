from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.services import get_user_language
from tgbot.states import RemoveFromBlacklist

remove_from_blacklist_cancel_router = Router()
remove_from_blacklist_cancel_router.message.filter(AdminFilter())


@remove_from_blacklist_cancel_router.callback_query(
    StateFilter(RemoveFromBlacklist), F.data == "cancel"
)
async def add_to_blacklist_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена добавления пользователя в чёрный список.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (AddToBlacklist).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value("remove-from-blacklist-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    try:
        await call.message.edit_text(text)
    except TelegramBadRequest:
        await call.message.edit_reply_markup()
