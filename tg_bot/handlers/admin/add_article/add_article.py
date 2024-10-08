from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import AddArticle

command_add_article_router = Router()


@command_add_article_router.message(Command("add_article"))
async def add_article(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("add-article-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddArticle.add_title)
