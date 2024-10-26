from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from config import config
from api.api_v1.schemas import UserSchema
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.middlewares import SaturdayMiddleware
from tg_bot.states import Saturday

command_saturday_router = Router()
command_saturday_router.message.middleware(SaturdayMiddleware())


@command_saturday_router.message(
    CommandStart(deep_link=True, magic=F.args.regexp("set"))
)
@command_saturday_router.message(Command("saturday"))
async def saturday(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    user: UserSchema,
):
    if user.is_premium:
        await message.answer(l10n.format_value("saturday-error-user-has-premium"))
        return

    await message.answer(
        l10n.format_value(
            "saturday-select-book-1",
            {
                "price_rub": config.price.set.rub,
                "price_xtr": config.price.set.xtr,
                "channel_link": config.channel.main_link,
            },
        ),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Saturday.select_book_1)
