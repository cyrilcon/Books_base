from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
from fluent.runtime import FluentLocalization

from config import config
from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import is_valid_book_article
from tg_bot.states import Saturday

saturday_step_2_router = Router()


@saturday_step_2_router.callback_query(
    StateFilter(Saturday.select_book_2),
    F.data == "back",
)
async def back_to_saturday_step_1(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    book_ids = data.get("book_ids")
    del book_ids[-1]

    await call.message.edit_text(
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
    await state.update_data(book_ids=book_ids)
    await state.set_state(Saturday.select_book_1)
    await call.answer()


@saturday_step_2_router.message(
    StateFilter(Saturday.select_book_2),
    F.text,
)
async def saturday_step_2(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    article_2 = message.text

    if not is_valid_book_article(article_2):
        await message.answer(
            l10n.format_value("saturday-error-invalid-article"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    id_book_2 = int(article_2.lstrip("#"))

    data = await state.get_data()
    book_ids = data.get("book_ids")

    if id_book_2 in book_ids:
        await message.answer(
            l10n.format_value("saturday-error-article-already-selected"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    response = await api.books.get_book_by_id(id_book=id_book_2)
    status = response.status

    if status != 200:
        await message.answer(
            l10n.format_value("saturday-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    user_book_ids = data.get("user_book_ids")

    book = response.get_model()

    if id_book_2 in user_book_ids:
        await message.answer(
            l10n.format_value(
                "saturday-error-user-already-has-this-book",
                {"title": book.title},
            ),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    title_1 = data.get("title_1")
    await message.answer(
        l10n.format_value(
            "saturday-select-book-3",
            {"title_1": title_1, "title_2": book.title},
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )

    book_ids.append(id_book_2)
    await state.update_data(book_ids=book_ids, title_2=book.title)
    await state.set_state(Saturday.select_book_3)
