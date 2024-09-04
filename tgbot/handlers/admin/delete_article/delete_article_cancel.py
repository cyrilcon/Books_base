from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.states import DeleteArticle

delete_article_cancel_router = Router()


@delete_article_cancel_router.callback_query(
    StateFilter(DeleteArticle), F.data == "cancel"
)
async def delete_article_cancel(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    text = l10n.format_value("delete-article-canceled")

    await state.clear()
    await call.answer(text, show_alert=True)
    await call.message.edit_text(text)
