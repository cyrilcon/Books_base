from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message
from fluent.runtime import FluentLocalization

from api.books_base_api import api
from tg_bot.config import config
from tg_bot.keyboards.inline import cancel_keyboard, back_cancel_keyboard
from tg_bot.services import ClearKeyboard, is_valid_book_article
from tg_bot.states import Saturday

saturday_step_1_router = Router()


@saturday_step_1_router.message(Command("saturday"))
async def saturday(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    sent_message = await message.answer(
        l10n.format_value(
            "saturday-select-book-1",
            {
                "price_rub": config.price.saturday.rub,
                "price_xtr": config.price.saturday.xtr,
            },
        ),
        reply_markup=cancel_keyboard(l10n),
    )
    await state.set_state(Saturday.select_book_1)

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )


@saturday_step_1_router.message(
    StateFilter(Saturday.select_book_1),
    F.text,
)
async def saturday_step_1(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    article_1 = message.text

    if not is_valid_book_article(article_1):
        sent_message = await message.answer(
            l10n.format_value("saturday-error-invalid-article"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    id_book_1 = int(article_1.lstrip("#"))

    response = await api.books.get_book_by_id(id_book=id_book_1)
    status = response.status

    if status != 200:
        sent_message = await message.answer(
            l10n.format_value("saturday-error-article-not-found"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    book = response.get_model()

    response = await api.users.get_book_ids(id_user=message.from_user.id)
    user_book_ids = response.result

    if id_book_1 in user_book_ids:
        sent_message = await message.answer(
            l10n.format_value("saturday-error-user-already-has-this-book"),
            reply_markup=cancel_keyboard(l10n),
        )
        await ClearKeyboard.safe_message(
            storage=storage,
            id_user=message.from_user.id,
            sent_message_id=sent_message.message_id,
        )
        return

    sent_message = await message.answer(
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

    await ClearKeyboard.safe_message(
        storage=storage,
        id_user=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
