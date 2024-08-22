from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import Serve

serve_from_button_router = Router()
serve_from_button_router.message.filter(AdminFilter())


@serve_from_button_router.callback_query(F.data.startswith("serve"))
async def serve_from_button(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    id_booking = int(call.data.split(":")[-1])

    response = await api.orders.get_booking_by_id(id_booking)
    status = response.status

    await call.answer(cache_time=1)

    if status == 200:
        booking = response.result
        await state.update_data(id_booking=booking["id_booking"])

        sent_message = await call.message.answer(
            l10n.format_value("serve-send-book-from-button"),
            reply_markup=cancel_keyboard(l10n),
        )
        await state.set_state(Serve.send_book)

        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=call.from_user.id,
            sent_message_id=sent_message.message_id,
        )
    else:
        await call.message.edit_reply_markup()
        await call.message.answer(l10n.format_value("serve-is-already-serviced"))
