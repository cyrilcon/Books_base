from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import view_orders_keyboard
from .get_order_info import get_order_info

command_view_orders_router = Router()


@command_view_orders_router.message(
    Command("view_orders"),
    flags={"safe_message": False},
)
async def view_orders(
    message: Message,
    l10n: FluentLocalization,
):
    orders_count, id_order, text = await get_order_info(l10n)

    if orders_count == 0:
        await message.answer(l10n.format_value("orders-absent"))
    else:
        await message.answer(
            text=text,
            reply_markup=view_orders_keyboard(
                l10n=l10n,
                id_order=id_order,
                orders_count=orders_count,
            ),
        )
