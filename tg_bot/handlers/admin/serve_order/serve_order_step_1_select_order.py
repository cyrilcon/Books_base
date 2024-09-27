from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import ClearKeyboard, create_user_link
from tg_bot.states import ServeOrder

serve_step_1_router = Router()


@serve_step_1_router.message(Command("serve_order"))
async def serve_order(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("serve-order-prompt-select-order"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(ServeOrder.select_order)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@serve_step_1_router.message(
    StateFilter(ServeOrder.select_order),
    F.text,
)
async def serve_order_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    order_number = message.text

    if order_number[0] == "№":
        order_number = order_number[1:]

    if not order_number.isdigit():
        sent_message = await message.answer(
            l10n.format_value("serve-order-error-invalid-order-number"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_order = int(order_number)

    response = await api.orders.get_order_by_id(id_order=id_order)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("serve-order-error-order-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    order = response.get_model()

    response = await api.users.get_user_by_id(order.id_user)
    user = response.get_model()
    id_user = user.id_user

    user_link = await create_user_link(user.full_name, user.username)

    sent_message = await message.answer(
        l10n.format_value(
            "serve-order-prompt-select-book",
            {
                "user_link": user_link,
                "id_user": str(id_user),
                "book_title": order.book_title,
                "author_name": order.author_name,
                "id_order": str(id_order),
            },
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(id_order=id_order)
    await state.set_state(ServeOrder.select_book)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
