from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tgbot.api.books_base_api import api
from tgbot.config import config
from tgbot.keyboards.inline import cancel_keyboard
from tgbot.services import ClearKeyboard
from tgbot.states import CancelOrder

cancel_order_router = Router()


@cancel_order_router.message(Command("cancel_order"))
async def cancel_order(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("cancel-order-select"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(CancelOrder.select_order)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@cancel_order_router.message(StateFilter(CancelOrder.select_order), F.text)
async def cancel_order_select(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    order_number = message.text
    id_user = message.from_user.id

    if order_number[0] == "№":
        order_number = order_number[1:]

    if not order_number.isdigit():
        sent_message = await message.answer(
            l10n.format_value("cancel-order-error-invalid-number"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_order = int(order_number)

    response = await api.orders.get_order_by_id(id_order)
    status = response.status
    order = response.result

    if status == 200 and (
        id_user == config.tg_bot.super_admin and id_user == order["id_user"]
    ):
        await api.orders.delete_order(id_order)

        await state.clear()
        await message.answer(
            l10n.format_value(
                "cancel-order-success",
                {"id_order": str(id_order), "book_title": order["book_title"]},
            ),
        )
        return

    sent_message = await message.answer(
        l10n.format_value("cancel-order-error-not-found"),
        reply_markup=cancel_keyboard(l10n),
    )
    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
