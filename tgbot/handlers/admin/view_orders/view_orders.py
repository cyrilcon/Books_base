from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.keyboards.inline import view_orders_keyboard
from tgbot.services import get_order_info

view_orders_router = Router()


@view_orders_router.message(Command("view_orders"))
async def view_orders(message: Message, l10n: FluentLocalization):
    orders_count, id_order, text = await get_order_info(l10n)

    if orders_count == 0:
        await message.answer(l10n.format_value("orders-absent"))
    else:
        await message.answer(
            text, reply_markup=view_orders_keyboard(l10n, id_order, orders_count)
        )


@view_orders_router.callback_query(F.data.startswith("order_position"))
async def order_position(call: CallbackQuery, l10n: FluentLocalization):
    position = int(call.data.split(":")[-1])

    orders_count, id_order, text = await get_order_info(l10n, position=position)

    if orders_count == 0:
        await call.message.edit_text(l10n.format_value("orders-absent"))
    else:
        await call.message.edit_text(
            text=text,
            reply_markup=view_orders_keyboard(
                l10n=l10n,
                id_order=id_order,
                orders_count=orders_count,
                position=position,
            ),
        )
    await call.answer()
