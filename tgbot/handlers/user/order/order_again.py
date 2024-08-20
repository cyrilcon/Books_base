from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import Order

order_again_router = Router()


@order_again_router.callback_query(F.data == "order_again")
async def order_again(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)

    sent_message = await call.message.answer(
        l10n.format_value("order-step-1-book-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Order.book_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()
