from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.services import get_user_language
from tgbot.states import ShareBase

share_base_cancel_router = Router()


@share_base_cancel_router.callback_query(F.data == "share_base_cancel")
@share_base_cancel_router.callback_query(StateFilter(ShareBase), F.data == "cancel")
async def share_base_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена отправки base пользователю.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (ShareBase).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value("share-base-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
