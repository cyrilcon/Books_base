from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import view_orders_keyboard
from .get_order_info import get_order_info

view_order_position_router = Router()


@view_order_position_router.callback_query(F.data.startswith("order_position"))
async def view_order_position(
    call: CallbackQuery,
    l10n: FluentLocalization,
):
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
