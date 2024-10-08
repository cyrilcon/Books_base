from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import DeleteArticle

command_delete_article_router = Router()


@command_delete_article_router.message(Command("delete_article"))
async def delete_article(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await message.answer(
        l10n.format_value("delete-article"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(DeleteArticle.select_article)
