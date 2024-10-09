from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import ShareBase

common_share_base_router = Router()


@common_share_base_router.message(Command("share_base"))
async def share_base(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("share-base"),
        reply_markup=cancel_keyboard(l10n),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await state.set_state(ShareBase.select_user)
