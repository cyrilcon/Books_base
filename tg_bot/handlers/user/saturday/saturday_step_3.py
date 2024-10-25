from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from config import config
from tg_bot.keyboards.inline import (
    cancel_keyboard,
    back_cancel_keyboard,
    buy_set_keyboard,
)
from tg_bot.services import is_valid_book_article
from tg_bot.states import Saturday

saturday_step_3_router = Router()


@saturday_step_3_router.callback_query(
    StateFilter(Saturday.select_book_3),
    F.data == "back",
)
async def back_to_saturday_step_2(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    data = await state.get_data()
    title_1 = data.get("title_1")
    book_ids = data.get("book_ids")
    del book_ids[-1]

    await call.message.edit_text(
        l10n.format_value(
            "saturday-select-book-2",
            {"title_1": title_1},
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.update_data(book_ids=book_ids)
    await state.set_state(Saturday.select_book_2)
    await call.answer()


@saturday_step_3_router.message(
    StateFilter(Saturday.select_book_3),
    F.text,
)
async def saturday_step_3(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    article_3 = message.text

    if not is_valid_book_article(article_3):
        await message.answer(
            l10n.format_value("saturday-error-invalid-article"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    id_book_3 = int(article_3.lstrip("#"))

    data = await state.get_data()
    book_ids = data.get("book_ids")

    if id_book_3 in book_ids:
        await message.answer(
            l10n.format_value("saturday-error-article-already-selected"),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    response = await api.books.get_book_by_id(id_book=id_book_3)
    status = response.status

    if status != 200:
        await message.answer(
            l10n.format_value("saturday-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    book = response.get_model()
    user_book_ids = data.get("user_book_ids")

    if id_book_3 in user_book_ids:
        await message.answer(
            l10n.format_value(
                "saturday-error-user-already-has-this-book",
                {"title": book.title},
            ),
            reply_markup=back_cancel_keyboard(l10n),
        )
        return

    book_ids.append(id_book_3)

    title_1 = data.get("title_1")
    title_2 = data.get("title_2")

    covers = []
    for id_book in book_ids:
        response = await api.books.get_book_by_id(id_book=id_book)
        book = response.get_model()
        covers.append(InputMediaPhoto(media=book.cover))

    await message.answer_media_group(media=covers)
    await message.answer(
        l10n.format_value(
            "saturday-success",
            {
                "title_1": title_1,
                "title_2": title_2,
                "title_3": book.title,
                "price_rub": config.price.set.rub,
                "price_xtr": config.price.set.xtr,
            },
        ),
        reply_markup=buy_set_keyboard(l10n, book_ids=book_ids),
    )
    await state.clear()
