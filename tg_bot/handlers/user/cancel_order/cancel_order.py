from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from api.books_base_api.schemas import UserSchema
from tg_bot.filters import AdminFilter
from tg_bot.keyboards.inline import orders_keyboard

command_cancel_order_router = Router()


@command_cancel_order_router.message(
    Command("cancel_order"),
    AdminFilter(),
    flags={"safe_message": False},
)
async def cancel_order_for_admin(
    message: Message,
    l10n: FluentLocalization,
):
    response = await api.orders.get_order_ids()
    orders = response.result

    if len(orders) == 0:
        await message.answer(l10n.format_value("orders-absent"))
        return

    await message.answer(
        l10n.format_value("cancel-order"),
        reply_markup=orders_keyboard(orders=orders),
    )


@command_cancel_order_router.message(
    Command("cancel_order"),
    flags={"safe_message": False},
)
async def cancel_order(
    message: Message,
    l10n: FluentLocalization,
    user: UserSchema,
):
    response = await api.users.get_order_ids_by_user(id_user=user.id_user)
    orders = response.result

    if len(orders) == 0:
        await message.answer(l10n.format_value("cancel-order-error-user-has-no-order"))
        return

    await message.answer(
        l10n.format_value("cancel-order"),
        reply_markup=orders_keyboard(orders=orders),
    )
