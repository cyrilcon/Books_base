from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services.users import create_user_link
from tg_bot.states import ServeOrder

serve_order_step_1_router = Router()


@serve_order_step_1_router.message(
    StateFilter(ServeOrder.select_order),
    F.text,
)
async def serve_order_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    order_number = message.text

    if order_number[0] == "№":
        order_number = order_number[1:]

    if not order_number.isdigit():
        await message.answer(
            l10n.format_value("serve-order-error-invalid-order-number"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    id_order = int(order_number)

    response = await api.orders.get_order_by_id(id_order=id_order)

    if response.status != 200:
        await message.answer(
            l10n.format_value("serve-order-error-order-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    order = response.get_model()

    response = await api.users.get_user_by_id(id_user=order.id_user)
    user = response.get_model()

    user_link = create_user_link(user.full_name, user.username)

    await message.answer(
        l10n.format_value(
            "serve-order-select-book",
            {
                "user_link": user_link,
                "id_user": str(user.id_user),
                "book_title": order.book_title,
                "author_name": order.author_name,
                "id_order": str(id_order),
            },
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(id_order=id_order)
    await state.set_state(ServeOrder.select_book)
