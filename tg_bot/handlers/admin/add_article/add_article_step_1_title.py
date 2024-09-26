from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import ClearKeyboard
from tg_bot.states import AddArticle

add_article_step_1_router = Router()


@add_article_step_1_router.message(Command("add_article"))
async def add_article(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value("add-article-prompt-title"),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(AddArticle.add_title)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@add_article_step_1_router.message(
    StateFilter(AddArticle.add_title),
    F.text,
)
async def add_article_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    title = message.text

    if len(title) > 255:
        sent_message = await message.answer(
            l10n.format_value("add-article-error-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    sent_message = await message.answer(
        l10n.format_value("add-article-prompt-link"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(title=title)
    await state.set_state(AddArticle.add_link)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
