from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.config import config
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import Saturday

command_saturday_router = Router()


@command_saturday_router.message(Command("saturday"))
async def saturday(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value(
            "saturday-select-book-1",
            {
                "price_rub": config.price.set.rub,
                "price_xtr": config.price.set.xtr,
            },
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Saturday.select_book_1)
