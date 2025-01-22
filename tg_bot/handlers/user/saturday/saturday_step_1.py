from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from tg_bot.api_client import api
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services.utils import is_valid_book_article
from tg_bot.states import Saturday

saturday_step_1_router = Router()


@saturday_step_1_router.message(
    StateFilter(Saturday.select_book_1),
    F.text,
)
async def saturday_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
):
    article_1 = message.text

    if not is_valid_book_article(article_1):
        await message.answer(
            l10n.format_value("saturday-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    id_book_1 = int(article_1.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book_1)

    if response.status != 200:
        await message.answer(
            l10n.format_value("saturday-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    book = response.get_model()

    response = await api.users.get_book_ids(id_user=message.from_user.id)
    user_book_ids = response.result

    if id_book_1 in user_book_ids:
        await message.answer(
            l10n.format_value(
                "saturday-error-user-already-has-this-book",
                {"title": book.title},
            ),
            reply_markup=cancel_keyboard(l10n),
        )
        return

    await message.answer(
        l10n.format_value(
            "saturday-select-book-2",
            {"title_1": book.title},
        ),
        reply_markup=back_cancel_keyboard(l10n),
    )

    book_ids = [id_book_1]
    await state.update_data(
        user_book_ids=user_book_ids,
        book_ids=book_ids,
        title_1=book.title,
    )
    await state.set_state(Saturday.select_book_2)
