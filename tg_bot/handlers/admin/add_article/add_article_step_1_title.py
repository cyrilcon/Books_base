from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.states import AddArticle

add_article_step_1_router = Router()


@add_article_step_1_router.message(
    StateFilter(AddArticle.add_title),
    F.text,
)
async def add_article_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    title = message.text

    if len(title) > 255:
        await message.answer(
            l10n.format_value("add-article-error-title-too-long"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await message.answer(
        l10n.format_value("add-article-link"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.update_data(title=title)
    await state.set_state(AddArticle.add_link)
