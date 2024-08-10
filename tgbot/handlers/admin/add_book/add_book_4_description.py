from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import Message, CallbackQuery
from fluent.runtime import FluentLocalization

from tgbot.filters import AdminFilter
from tgbot.keyboards.inline import (
    back_cancel_keyboard,
    done_clear_back_cancel_keyboard,
)
from tgbot.services import ClearKeyboard
from tgbot.states import AddBook

add_book_router_4 = Router()
add_book_router_4.message.filter(AdminFilter())


@add_book_router_4.callback_query(
    StateFilter(AddBook.add_description), F.data == "back"
)
async def back_to_add_book_3(
    call: CallbackQuery,
    l10n: FluentLocalization,
    state: FSMContext,
):
    await call.answer(cache_time=1)
    await call.message.edit_text(
        l10n.format_value("add-book-authors"),
        reply_markup=back_cancel_keyboard(l10n),
    )
    await state.set_state(AddBook.add_authors)


@add_book_router_4.message(StateFilter(AddBook.add_description), F.text)
async def add_book_4(
    message: Message,
    l10n: FluentLocalization,
    state: FSMContext,
    storage: RedisStorage,
):
    await ClearKeyboard.clear(message, storage)

    description = message.text

    if len(description) <= 850:
        data = await state.get_data()
        genres = data.get("genres")

        if genres:
            genres = " ".join(["#" + genre["genre"] for genre in genres])
            sent_message = await message.answer(
                l10n.format_value(
                    "add-book-genres-more",
                    {"genres": genres},
                ),
                reply_markup=done_clear_back_cancel_keyboard(l10n),
            )
        else:
            sent_message = await message.answer(
                l10n.format_value("add-book-genres"),
                reply_markup=back_cancel_keyboard(l10n),
            )

        await state.update_data(description=description)
        await state.set_state(AddBook.add_genres)
    else:
        sent_message = await message.answer(
            l10n.format_value("description-too-long"),
            reply_markup=back_cancel_keyboard(l10n),
        )

    await ClearKeyboard.safe_message(
        storage=storage,
        user_id=message.from_user.id,
        sent_message_id=sent_message.message_id,
    )
