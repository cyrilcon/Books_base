from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import Order

command_order_router = Router()


@command_order_router.message(Command("order"))
async def order(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("order"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Order.book_title)
