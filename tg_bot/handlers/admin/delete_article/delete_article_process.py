import re

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.states import DeleteArticle

delete_article_process_router = Router()


@delete_article_process_router.message(
    StateFilter(DeleteArticle.select_article),
    F.text,
)
async def delete_article_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    link = message.text

    if not re.match(r"^(https://)?telegra\.ph/", link):
        await message.answer(
            l10n.format_value("delete-article-error-invalid-link"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    response = await api.articles.get_article_by_link(link=link)

    if response.status != 200:
        await message.answer(
            l10n.format_value("delete-article-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    article = response.get_model()
    await api.articles.delete_article(id_article=article.id_article)

    await message.answer(l10n.format_value("delete-article-success"))
    await state.clear()
