from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import Support

support_reply_to_admin_router = Router()


@support_reply_to_admin_router.callback_query(F.data == "reply_to:admin")
async def support_reply_to_admin(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await call.answer(cache_time=1)
    sent_message = await call.message.answer(
        l10n.format_value("support-reply-to-admin"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(from_button=True)
    await state.set_state(Support.reply_to_admin)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
