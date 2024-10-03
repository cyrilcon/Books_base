from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.filters import AdminFilter
from tg_bot.services import ClearKeyboard
from .keyboards import orders_keyboard

cancel_order_router = Router()


@cancel_order_router.message(
    Command("cancel_order"),
    AdminFilter(),
)
async def cancel_order(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    response = await api.orders.get_order_ids()
    orders = response.result

    if len(orders) == 0:
        await message.answer(l10n.format_value("orders-absent"))
        return

    await message.answer(
        l10n.format_value("cancel-order"),
        reply_markup=orders_keyboard(orders=orders),
    )


@cancel_order_router.message(Command("cancel_order"))
async def cancel_order(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)
    await state.clear()

    id_user = message.from_user.id

    response = await api.users.get_order_ids_by_user(id_user=id_user)
    orders = response.result

    if len(orders) == 0:
        await message.answer(l10n.format_value("cancel-order-error-user-has-no-order"))
        return

    await message.answer(
        l10n.format_value("cancel-order"),
        reply_markup=orders_keyboard(orders=orders),
    )


@cancel_order_router.callback_query(F.data.startswith("cancel_order"))
async def cancel_order_process(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(call, storage)
    await state.clear()

    id_order = int(call.data.split(":")[-1])
    id_user = call.from_user.id

    response = await api.orders.get_order_by_id(id_order=id_order)
    status = response.status

    response = await api.users.get_user_by_id(id_user=id_user)
    user = response.get_model()

    if user.is_admin:
        response = await api.orders.get_order_ids()
    else:
        response = await api.users.get_order_ids_by_user(id_user=id_user)
    orders = response.result

    if status != 200:
        await call.answer(
            l10n.format_value("cancel-order-error-order-already-canceled"),
            show_alert=True,
        )
        await call.message.edit_reply_markup(
            reply_markup=orders_keyboard(orders=orders)
        )
        return

    await api.orders.delete_order(id_order=id_order)

    await call.message.edit_text(
        l10n.format_value(
            "cancel-order-success",
            {"id_order": str(id_order)},
        ),
        reply_markup=orders_keyboard(orders=orders),
    )
    await call.answer()
