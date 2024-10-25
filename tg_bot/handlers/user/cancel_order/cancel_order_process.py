from aiogram import Router, F
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.api_client.schemas import UserSchema
from tg_bot.keyboards.inline import orders_keyboard

cancel_order_process_router = Router()


@cancel_order_process_router.callback_query(
    F.data.startswith("cancel_order"),
    flags={
        "clear_keyboard": False,
        "safe_message": False,
    },
)
async def cancel_order_process(
    call: CallbackQuery,
    l10n: FluentLocalization,
    user: UserSchema,
):
    id_order = int(call.data.split(":")[-1])

    response = await api.orders.get_order_by_id(id_order=id_order)
    status = response.status

    if user.is_admin:
        response = await api.orders.get_order_ids()
    else:
        response = await api.users.get_order_ids_by_user(id_user=user.id_user)
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

    if user.is_admin:
        response = await api.orders.get_order_ids()
    else:
        response = await api.users.get_order_ids_by_user(id_user=user.id_user)
    orders = response.result

    await call.message.edit_text(
        l10n.format_value(
            "cancel-order-success",
            {"id_order": str(id_order)},
        ),
        reply_markup=orders_keyboard(orders=orders),
    )
    await call.answer()
