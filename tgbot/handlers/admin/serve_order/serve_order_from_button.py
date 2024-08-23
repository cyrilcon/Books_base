from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import ServeOrder

serve_from_button_router = Router()


@serve_from_button_router.callback_query(F.data.startswith("serve_order"))
async def serve_order_from_button(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    id_order = int(call.data.split(":")[-1])

    response = await api.orders.get_order_by_id(id_order)
    status = response.status

    if status != 200:
        await call.message.edit_reply_markup()
        await call.message.answer(
            l10n.format_value("serve-order-error-order-already-served")
        )
        return

    order = response.get_model()
    await state.update_data(id_order=order.id_order)

    sent_message = await call.message.answer(
        l10n.format_value("serve-order-prompt-select-book-from-button"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(ServeOrder.select_book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )

    await call.answer()
