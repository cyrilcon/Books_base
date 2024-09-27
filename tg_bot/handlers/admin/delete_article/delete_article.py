import re

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.keyboards.inline import cancel_keyboard
from tg_bot.services import ClearKeyboard
from tg_bot.states import DeleteArticle

delete_article_router = Router()


@delete_article_router.message(Command("delete_article"))
async def delete_article(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("delete-article-prompt-link"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(DeleteArticle.select_article)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@delete_article_router.message(
    StateFilter(DeleteArticle.select_article),
    F.text,
)
async def delete_article_process(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    link = message.text

    if not re.match(r"^(https://)?telegra\.ph/", link):
        sent_message = await message.answer(
            l10n.format_value("delete-article-error-invalid-link"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    response = await api.articles.get_article_by_link(link)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("delete-article-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    article = response.get_model()
    await api.articles.delete_article(article.id_article)

    await message.answer(l10n.format_value("delete-article-success"))
    await state.clear()
