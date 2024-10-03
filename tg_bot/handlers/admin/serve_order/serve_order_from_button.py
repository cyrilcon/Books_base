from aiogram import Router, F, Bot
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, reply_keyboard
from tg_bot.services import ClearKeyboard, get_user_localization
from tg_bot.states import ServeOrder

serve_from_button_router = Router()


@serve_from_button_router.callback_query(F.data.startswith("serve_order"))
async def serve_order_from_button(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    id_order = int(call.data.split(":")[-1])

    response = await api.orders.get_order_by_id(id_order=id_order)
    status = response.status

    if status != 200:
        await call.message.edit_reply_markup()
        await call.message.answer(
            l10n.format_value("serve-order-error-order-already-served-or-canceled")
        )
        return

    await state.update_data(id_order=id_order)

    sent_message = await call.message.answer(
        l10n.format_value("serve-order-select-book-from-button"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(ServeOrder.select_book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=call.from_user.id,
        sent_message_id=sent_message.message_id,
    )
    await call.answer()


@serve_from_button_router.callback_query(F.data.startswith("book_unavailable"))
async def serve_order_book_unavailable(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
    bot: Bot,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()
    await call.message.edit_reply_markup()

    id_order = int(call.data.split(":")[-1])

    response = await api.orders.get_order_by_id(id_order=id_order)
    order = response.get_model()

    l10n_recipient = await get_user_localization(id_user=order.id_user)
    try:
        await bot.send_message(
            chat_id=order.id_user,
            text=l10n_recipient.format_value(
                "serve-order-book-unavailable",
                {
                    "id_order": str(id_order),
                    "book_title": order.book_title,
                    "author_name": order.author_name,
                },
            ),
            reply_markup=reply_keyboard(l10n),
        )
    except AiogramError:
        await call.message.answer(l10n.format_value("error-user-blocked-bot"))
    else:
        await call.message.answer(l10n.format_value("serve-order-message-sent"))
    await api.orders.delete_order(id_order=id_order)
    await call.answer()
