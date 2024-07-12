from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from tgbot.filters import AdminFilter
from tgbot.services import get_user_language
from tgbot.states import GivePremium

give_premium_cancel_router = Router()
give_premium_cancel_router.message.filter(AdminFilter())


@give_premium_cancel_router.callback_query(StateFilter(GivePremium), F.data == "cancel")
async def give_premium_cancel(call: CallbackQuery, state: FSMContext):
    """
    Отмена присвоения статуса Books_base Premium.
    :param call: Нажатая кнопка "Отмена".
    :param state: FSM (GivePremium).
    """

    id_user = call.from_user.id
    l10n = await get_user_language(id_user)
    text = l10n.format_value("give-premium-cancel")

    await state.clear()
    await call.answer(text, show_alert=True)
    try:
        await call.message.edit_text(text)
    except TelegramBadRequest:
        await call.message.edit_reply_markup()
